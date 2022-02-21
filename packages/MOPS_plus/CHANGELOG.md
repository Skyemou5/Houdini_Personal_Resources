---
title: MOPs+ Changelog
subtitle: 
description:
featured_image: ''
---

For open source MOPs release notes, please see the Releases page on [GitHub](https://github.com/toadstorm/MOPS/releases).

## 2021-09-30
* Added a Pivot option to **MOPs Filter**.
* Added documentation to **MOPs Filter**.
* Fixed a bug in **MOPs Filter** that threw an error when the Extra Attributes field was empty or pointed to no valid attributes.
* Fixed a licensing bug on OSX and Linux systems.
* Modified the default JSON package file to prevent annoying Python warnings in future versions of Houdini.


## 2021-09-13
* Added **MOPs Filter**, a SOPs-based temporal filter for any float or vector3/4 point attributes.
* **MOPs Typography** now properly exports primitive groups when in Chisel mode.

## 2021-08-20
* Massively improved the speed of all MOPsDOPs. 
* Improved selection handle behavior on **MOPs Edit**. It should now behave much more naturally when selecting and re-selecting objects.
* Improved the cooking efficiency of **MOPs Edit**, especially when lots of edits are done in a single node.


## 2021-08-12
* First official Python 3 release!
* Updated all internal scripts for compatibility with OSX running Python 3.
* Added static collider option to **MOPs Deintersect** and exposed some other Bullet parameters.
* Improved position constraints in **MOPs Deintersect** when dealing with pivots not already at the center of mass.
* **MOPs Collision Geo** now has a "Treat As Solid" option for convex decomposition.

## 2021-07-31
* Fixed a group mask bug in **MOPs Move Along Spline DOP** that prevented multiple copies of the node from working in succession.

## 2021-07-14
* Fixed a bug in **MOPs Edit** that caused the wrong primitives to move if a primitive upstream was deleted. 
* **MOPs Edit** now has built-in viewport handle cycling using the user’s existing bound hotkey (defaults to “M”).
* **MOPs Camera Blender** now allows the use of external paths when in “Camera Index” mode.
* **MOPs Camera Blender** now tries to create the initial blended camera in a better network position.
* Added a group mask parameter to **MOPs Collision Geo**.


## 2021-06-28
* Fixed a bug that could cause **MOPs+ Camera Blender** not to function due to a node or parameter synchronization error.

## 2021-06-25
* The "Bake Camera" button on the **MOPs+ Camera Blender** now matches all available parameters to the original camera, including those not interpolated.
* Channel links are automatically generated when the "Extra Attributes" parameter is added to.
* Improved **MOPs+ Camera Blender** interpolation when "Maintain Pivot" is enabled and there's less than three camera inputs.

## 2021-06-15
* Greatly improved the smoothness and stability of **MOPs+ Camera Blender**, especially when "Maintain Pivot" is enabled. There should be significantly less bumps in most camera movements.
* Added a new example file, "camera_blender_new" that shows off a little more of what you can do with the node.

## 2021-06-08
* Added "Maintain Focus Distance" option to **MOPs+ Camera Blender**. This forces the blended camera to maintain the blended Focus Distance from the source cameras as it interpolates between them.
* Modified Smoothing options on **MOPs+ Camera Blender**.
* Fixed an interpolation issue that could cause flipping on some cameras when blending over a 180-degree rotation.
* Fixed a bug that could incorrectly modify composition guides if an external camera path had color or template point attributes.

## 2021-06-06
* The **MOPs+ Attribute Mapper** now supports drag-drop reordering of table rows.
* **MOPs+ Greeble** can now output groups for "front" and "side" faces.
* Updated the undo state for **MOPs+ Edit**. This should make undo operations more predictable.
* Added preliminary VEXpression support to **MOPs+ Move Along Spline DOP**.

## 2021-05-17
* The **MOPs+ Camera Blender** composition guides now correctly follow the camera when Filtering options are enabled.
* Added a "Frequency Scale" attribute option to **MOPs Waveforms**.
* Fixed Python 3 compatibility with **MOPs Waveforms**.

## 2021-04-21
* Added **MOPs+ Magnetize**.
* Added Filtering options to **MOPs+ Camera Blender**.
* Fixed a broken channel reference in **MOPs+ Camera Blender** that prevented rotation order from being properly applied in Euler mode.

## 2021-04-08
* Fixed a bug in **MOPs Apply Attributes DOP** that caused object scales to be reset when applying forces in "Position/Rotation" mode.
* Updated the rotation behavior in **MOPs Noise Modifier DOP** to be smoother with less flipping.
* Improved aiming behavior in **MOPs Aim** to be more consistent with less flipping.
* Fixed a bug in **MOPs Roll DOP** that prevented rolling from happening before collisions, even with "Wait for Collisions" disabled.
* Updated the `pops_roll` example file.
* **MOPs Stepper** now has a "Uniform" toggle for vector parameters.
* The **MOPs Fetch Attribute DOP** group parameter now has a dropdown to find groups from the processed object.
* Fixed an activation bug that would throw an error if a user tried to activate when any network viewer was not in Object or Geometry contexts.

## 2021-04-02
* Added Local Axis controls to **MOPs+ Aim DOP**. This allows you to more precisely choose your local forward and up vectors.
* Added revised "Camera Index" mode to **MOPs+ Camera Blender**. This allows you to blend cameras based on the camera number instead of a normalized 0-1 value.
* Added "Attribute Detach" options to **MOPs+ Move Along Spline DOP**. This allows you to detach from the path based on an attribute threshold.
* Made several bugfixes to **MOPs+ Apply Attributes DOP** to create more predictable behavior, especially when chaining multiple MOPsDOPs and POP forces together.
* The **MOPs+ Attribute Mapper** can now apply operator or file paths to multiple rows at once by selecting rows before clicking the selector button.
* Added a "Normalize Attribute" button to **MOPs+ Attribute Mapper**. This quickly normalizes a float attribute's values in the table for easy use with Falloffs.
* Fixed composition guide thickness in **MOPs+ Camera Blender**.
* Added an example file for **MOPs+ Aim DOP**.
* Added an example file for **MOPs+ Fetch Attributes** and Vellum constraints. This shows how to use **MOPs+ Fetch Attributes** to easily modify constraint attributes mid-simulation.
* Added an example file for **MOPs+ Stepper**.
* Added an instance path example network to the **MOPs+ Attribute Mapper** example file. This shows how you can use the Mapper to influence instance paths.
* Updated **MOPs+ Attribute Mapper** documentation with a visual guide.

## 2021-03-26
* Added the MOPs+ Stepper SOP. This quantizes transform and other point attributes to fixed intervals (i.e. 45-degree or 0.1-unit increments).
* Made several improvements to **MOPs Camera Blender**:
    1. Removed "Fit Type" parameter. The "Accurate" fit type is now the default and only interpolation mode.
    2. Improved the camera interpolation so that with default settings the path will always pass perfectly through each input camera.
    3. Paths are now properly calculated for 2-camera and 3-camera setups. Paths are by necessity linear in these situations; you must use post-smoothing options or a custom path for 3-camera setups (this is because Bezier curves require at least four control points).
    4. Added post-interpolation path smoothing options.
    5. Added an "Export Raw Path" button to go with the "Export Path" button. This allows you to start from an interpolated path when customizing.
    6. Added `camera_blender_custom.hip` to the examples. This shows how to use other MOPs nodes to influence a custom camera path.

## 2021-03-22
* Added a new default "Accurate" interpolation mode to **MOPs Camera Blender**. This can be controlled via the "Fit Type" parameter.
* Added the ability to change the visible thickness of composition guides in **MOPs Camera Blender**.

## 2021-03-14
* Added **MOPs+ Camera Blender.**

## 2021-03-03
* Added "Pulse" function to **MOPs Waveforms**.
* Fixed a bug in **MOPsDOPs Apply Attributes** that mistakenly set `id` attribute -1 in Vellum and other particle simulations.
* Fixed Python3 compatibility in **MOPs Shape Falloff DOP**.
* Made several changes to **MOPs RBD Runtime Constraints**:
    1. The Mask parameter now requires both objects involved in an impact to be included in the Mask for a collision to register. This excludes static objects like Ground Plane DOPs.
    2. The constraint orientation is now based on the `p@orient` attribute instead of the transform intrinsic. This should result in more stable orientations on impact.
    3. This DOP can now differentiate correctly between multiple DOP objects in collisions.


## 2021-02-06
* Added **MOPs RBD Runtime Constraints DOP**.
* Added **MOPs Waveforms**.
* Added example files for the two new operators.
* Fixed a bug in **MOPs+ Combine Falloffs** that prevented DOP Falloffs from functioning in Python3 builds of Houdini.

## 2021-01-22
* Scaling in both local and world space, with support for the `mops_orient` attribute, now works properly in **MOPs+ Apply Attributes DOP**, to match the recent changes to MOPs Apply Attributes SOP.
* Fixed a bug that caused Houdini to crash while collapsing **MOPs+ Typography** into a subnet in Python 2 builds of Houdini.
* Fixed the "Inside", "Outside" and "Surface Distance" modes on **MOPs+ Object Falloff DOP.**

## 2021-01-14
* Added MOPs Fetch Attribute DOP.

## 2021-01-13
* Fixed a bug in MOPs Typography and MOPs Edit that prevented compatibility with Python 3 builds of Houdini.
* Fixed a bug in MOPs Typography that caused letter index attributes to be generated incorrectly with multi-line text imported from a file.

## 2021-01-02
* Refactored all Python code for Python 3 compatibility. Note that this change will cause the stored table data in **MOPs Attribute Mapper** to be invalid. You will need to repopulate any MOPs Attribute Mapper tables. Apologies for the inconvenience.
* Fixed a bug in the Activation process that threw an error if the button was clicked outside a SOP network.

## 2020-12-31
* Fixed an unlikely bug in the Apply Attributes DOP that could break snapping behavior.
* Fixed bug in activation that threw an error when trying to re-activate an activated license.
* Clarified activation procedure.
