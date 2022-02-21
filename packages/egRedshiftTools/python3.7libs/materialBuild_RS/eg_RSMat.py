#####################################
#             LICENSE               #
#####################################
#
# Copyright (C) 2020  Elmar Glaubauf
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
This script will create a Redshift Material

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import hou


class RSMat():
    """Creates an RS-Material in the given context with a Name"""
    def __init__(self, context=hou.node("/mat"), name="RedshiftMaterial", files=None):

        # Variables used by Class
        self.img = ""

        # RS Material
        self.material_builder = None
        self.rs_mat = None
        self.redshift_material = None

        self.files = files
        self.context = context
        self.name = name

        self.cc_diffuse = False
        self.diff_linear = False

    def get_material_builder(self):
        """Returns the MaterialBuilder"""
        return self.material_builder

    def get_rsMat(self):
        return self.rs_mat

    def get_path(self):
        """Returns the Path to the MaterialBuilder"""
        return self.material_builder.path()

    def get_displace(self):
        """Checks if there is a Displacement applied"""
        if self.files["displace"]:
            return True
        else:
            return False

    def get_files(self):
        """Gets the Files withing the Materials as Dict"""
        return self.files

    def create_material(self, cc_diffuse=False, diff_linear=False, triplanar=False):
        """Creates an RS-Material in the given context"""
        self.cc_diffuse = cc_diffuse
        self.diff_linear = diff_linear
        self.triplanar = triplanar

        # RS Material Builder
        self.material_builder = self.context.createNode("redshift_vopnet")
        self.material_builder.setName(self.name, True)
        self.material_builder.moveToGoodPosition()

        # RS Material
        self.redshift_material = self.material_builder.children()[0]
        self.rs_mat = self.material_builder.glob("Material*")[0] # self.material_builder.createNode('redshift::Material')
        self.redshift_material.setInput(0, self.rs_mat, 0)

        if self.files:
            self.create_layers()

        self.material_builder.layoutChildren()

    def create_layers(self):
        """Creates Layers for the MaterialNode"""
        if self.files["basecolor"]:
            diff = None
            cc = None
            # User Setting - Create Triplanar

            if self.cc_diffuse:  # User Setting - Create ColorCorrecter
                cc = self.insertCC(self.material_builder, self.rs_mat, "diffuse_color")
                diff = self.create_texture(self.material_builder, cc, self.files["basecolor"], "Base_Color")
            else:
                diff = self.create_texture(self.material_builder, self.rs_mat, self.files["basecolor"], "Base_Color")
            if self.diff_linear:  # User Setting - Diffuse is Linear
                diff.parm("tex0_gamma").set(1)
            if self.files["ao"]:
                if self.cc_diffuse:  # User Setting - Create ColorCorrecter
                    self.create_texture(self.material_builder, self.rs_mat, self.files["ao"], "Ambient_Occlusion", cc)
                else:
                    self.create_texture(self.material_builder, self.rs_mat, self.files["ao"], "Ambient_Occlusion")
            if self.triplanar:
               tri = self.insertTriplanar(self.material_builder, self.rs_mat, "diffuse_color")
        if self.files["roughness"]:
            if self.triplanar:
                tri = self.insertTriplanar(self.material_builder, self.rs_mat, "refl_roughness")
                self.create_texture(self.material_builder, tri, self.files["roughness"], "Roughness", True)
            else:
                self.create_texture(self.material_builder, self.rs_mat, self.files["roughness"], "Roughness")

        if self.files["metallic"]:
            if self.triplanar:
                tri = self.insertTriplanar(self.material_builder, self.rs_mat, "refl_metalness")
                self.create_texture(self.material_builder, tri, self.files["metallic"], "Metallic", True)
            else:
                self.create_texture(self.material_builder, self.rs_mat, self.files["metallic"], "Metallic")
            self.rs_mat.parm("refl_fresnel_mode").set("2")

        if self.files["reflect"]:
            if self.triplanar:
                tri = self.insertTriplanar(self.material_builder, self.rs_mat, "refl_weight")
                self.create_texture(self.material_builder, tri, self.files["reflect"], "Reflectivity", True)
            else:
                self.create_texture(self.material_builder, self.rs_mat, self.files["reflect"], "Reflectivity")
        if self.files["normal"]:
            self.create_normal(self.material_builder, self.rs_mat, self.files["normal"], "Normal")
        if self.files["bump"]:
            self.create_bump(self.material_builder, self.rs_mat, self.files["bump"], "Bump")
        if self.files["displace"]:
            self.create_displace(self.material_builder, self.redshift_material, self.files["displace"], "Displacement")
            self.displaceFlag = 1

    def insertCC(self, parent, connector, channel):
        cc = parent.createNode("redshift::RSColorCorrection")
        connector.setNamedInput(channel, cc, 0)
        return cc

    def insertTriplanar(self, parent, connector, channel):
        if channel == "diffuse_color":
            inputNode = connector.input(0)
            tri = parent.createNode("redshift::TriPlanar")
            connector.setNamedInput(channel, tri, 0)
            tri.setFirstInput(inputNode, 0)
            return tri
        tri = parent.createNode("redshift::TriPlanar")
        connector.setNamedInput(channel, tri, 0)
        return tri

    def create_texture(self, parent, connector, channel, channelName, node_before=None):
        """Creates and connects a Texture"""
        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)

        if channelName == "Base_Color":
            connector.setFirstInput(tex, 0)
            tex.parm("tex0_colorSpace").set("sRGB")
            tex.parm("tex0_gamma").set("2.2")
        elif channelName == "Roughness":
            if node_before:
                connector.setFirstInput(tex,0)
            else:
                connector.setNamedInput("refl_roughness", tex, 0)
            tex.parm("tex0_colorSpace").set("Raw")
            tex.parm("tex0_gamma").set("1")
        elif channelName == "Metallic":
            if node_before:
                connector.setFirstInput(tex,0)
            else:
                connector.setNamedInput("refl_metalness", tex, 0)
            # Enable Metalness Model
            connector.parm("refl_fresnel_mode").set('2')
            tex.parm("tex0_colorSpace").set("Raw")
            tex.parm("tex0_gamma").set("1")
        elif channelName == "Reflectivity":
            if node_before:
                connector.setFirstInput(tex,0)
            else:
                connector.setNamedInput("refl_weight", tex, 0)
            tex.parm("tex0_colorSpace").set("Raw")
            tex.parm("tex0_gamma").set("1")
        elif channelName == "Ambient_Occlusion":
            mult = parent.createNode("redshift::RSMathMulVector")
            tex.parm("tex0_colorSpace").set("Raw")
            tex.parm("tex0_gamma").set("1")
            connector.setFirstInput(mult, 0)
            if node_before:
                mult.setInput(0, node_before, 0)
            else:
                bc = parent.glob("Base_Color")[0]
                mult.setInput(0, bc, 0)
            mult.setInput(1, tex, 0)
        if self.is_linear(channel):
            tex.parm("tex0_gamma").set(1)
        return tex

    def create_normal(self, parent, connector, channel, channelName):
        """Creates and connects a NormalMap"""
        # Create Bump Node

        bmp = parent.createNode("redshift::BumpMap")

        # Connect Things
        connector.setNamedInput("bump_input", bmp, 0)

        tex = parent.createNode("redshift::TextureSampler")
        tex.parm("tex0").set(channel)
        tex.parm("tex0_colorSpace").set("Raw")
        tex.parm("tex0_gamma").set("1")

        if self.triplanar:
            tri = parent.createNode("redshift::TriPlanar")
            bmp.setFirstInput(tri, 0)
            tri.setFirstInput(tex, 0)
        else:
            bmp.setFirstInput(tex, 0)
        bmp.parm("inputType").set("1")
        return

    def create_displace(self, parent, connector, channel, channelName):
        """Creates and connects a DisplacementMap"""
        # Create Displace Node
        displace = parent.createNode("redshift::Displacement")
        connector.setNamedInput("Displacement", displace, 0)

        # Create Tex
        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)
        tex.parm("tex0_gamma").set('1')

        
        if self.triplanar:
            tri = parent.createNode("redshift::TriPlanar")
            displace.setFirstInput(tri, 0)
            tri.setFirstInput(tex, 0)
        else:
            displace.setFirstInput(tex, 0)
        return

    def create_bump(self, parent, connector, channel, channelName):
        """Creates and connects a BumpMap"""
        # Create Bump Node
        bump = parent.createNode("redshift::BumpMap")
        connector.setNamedInput("bump_input", bump, 0)

        # Create Tex
        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)
        tex.parm("tex0_colorSpace").set("Raw")
        tex.parm("tex0_gamma").set("1")

        if self.triplanar:
            tri = parent.createNode("redshift::TriPlanar")
            bump.setFirstInput(tri, 0)
            tri.setFirstInput(tex, 0)
        else:
            bump.setFirstInput(tex, 0)
        return

    def is_linear(self, channel):
        """Check if the File is linear"""
        if channel.endswith("hdr"):
            return True
        if channel.endswith("exr"):
            return True
        return False