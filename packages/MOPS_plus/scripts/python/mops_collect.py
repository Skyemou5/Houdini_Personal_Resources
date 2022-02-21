import re
import os
import hou
import logging

FORMAT = '+-- %(name)-13s | %(levelname)-8s %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
logging.basicConfig(format=FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)
log = logging.getLogger("mops_collect")

def get_all_file_dependencies():
	# get all non-default dependent files and return them in some useful way.
	refs = hou.fileReferences()
	# this returns a tuple of Parm, string objects.
	# any returned file paths need to be expanded to sequences, if required.
	dependencies = {
		"hda": list(),
		"file": dict(),
	}
	seq_flags = ["$F", "$FF", "$SF", "$ST", "$T", "$N"]
	seq_file_regex_str = "^([\S]+[\._])(\$\w[\d]?)([\._][\S]+$)"
	seq_file_regex = re.compile(seq_file_regex_str)
	test_file_regex_str = "^([\S]+[\._])(\d)+([\._][\S]+$)"
	test_file_regex = re.compile(test_file_regex_str)
	log.debug("testing")

	for ref in refs:
		full_path = ref[1] if ref[0] is None else ref[0].eval()
		raw_path = ref[1]
		# ref[0] is a hou.Parm reference.
		# if ref[0] is None, ref[1] is going to be an HDA.
		# if it's not an HDA, it could be a file on disk, an op: reference,
		# or a path like "voptype.h voplib.h" which should be ignored.
		# the file on disk would need to be expanded to a sequence at some point.
		# for any parms containing $F, $FF, $SF, $ST or $N, maybe substitute with a wildcard and grab everything?
		# wedges would be likely impossible to parse, but those are rarely used for reads anyways.
		# maybe include a warning for those?
		# ref[1] is always going to be the expanded string.
		if ref[0] is None:
			dependencies["hda"].append(hou.text.expandString(ref[1]))
		else:
			# figure out if this is a dependency we care about or not.
			# if houdini can expand the string into a full file path, it matters.
			# only catch is that a sequence might not exist if the playbar isn't
			# currently on an active frame.
			ref_paths = list()

			full_path = hou.text.expandString(ref[1])
			log.debug("Found file dependency: {}".format(ref[1]))
			log.debug("Full path: {}".format(full_path))
			if not os.path.exists(full_path):
				continue
			if not os.path.isfile(full_path):
				continue

			if any(flag in ref[1] for flag in seq_flags):
				# this is a sequence... search the parent path.
				log.debug("testing sequence {}".format(ref[1]))
				base_path = os.path.dirname(full_path)
				test_files = os.listdir(base_path)
				# print("files found in path: {}".format(test_files))

				# test each file to see if it would fit the ref[1] path mask.
				# we already know that the directory will line up, so let's just run the regex against
				# the basename of the file(s).
				source_file_match = seq_file_regex.match(os.path.basename(ref[1]))
				if source_file_match is None:
					log.debug("source file basename {} doesn't match the sequence regex.".format(os.path.basename(ref[1])))
					continue
				log.debug("source file match groups: {}".format(source_file_match.groups()))
				if not source_file_match.groups():
					continue
				if test_files:
					for file in test_files:
						log.debug("testing file {}".format(file))
						test_file_match = test_file_regex.match(file)
						# if groups[0] and groups[2] are identical between this and the source file, this is a match
						if test_file_match is None:
							continue
						if test_file_match.groups():
							log.debug("test file match groups: {}".format(test_file_match.groups()))
							if len(test_file_match.groups()) == 3:
								if test_file_match.groups()[0] == source_file_match.groups()[0] and test_file_match.groups()[2] == source_file_match.groups()[2]:
									add_file = os.path.join(base_path, file).replace("\\", "/")
									ref_paths.append(add_file)
									log.info("Adding sequence file {} to parm {}/{}".format(add_file, ref[0].node().name(), ref[0].name()))
			else:
				ref_paths.append(full_path)
				log.info("Adding standalone file {} to parm {}/{}".format(full_path, ref[0].node().name(), ref[0].name()))
			# now let's add this to our dependencies.
			if ref_paths:
				dependencies["file"][ref[0]] = ref_paths
	return dependencies
