# coding=utf-8
from __future__ import absolute_import


import time
import datetime
import octoprint.plugin
import octoprint.printer
import re

import flask


class PrusaLevelingGuidePlugin(octoprint.plugin.SimpleApiPlugin,
							octoprint.plugin.SettingsPlugin,
							octoprint.plugin.AssetPlugin,
							octoprint.plugin.TemplatePlugin,
							octoprint.plugin.StartupPlugin):
	
	
	def on_after_startup(self):
		self.mesh_values = []
		self.bed_variance = None
		self.relative_values = []
		self.last_result = None
		self.regex = re.compile(r"^(  -?\d+.\d+)+$")
		self.waiting_for_response = False
		self.sent_time = False


	##~~ SimpleApiPlugin mixin
	def on_api_get(self, request):
		return flask.jsonify(bed_variance=self.bed_variance,
							values=self.relative_values,
							last_result=self.last_result)

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			mesh_gcode = 'G28 W ; home all without mesh bed level\nM400\nG80 N3; mesh bed leveling\nG81 ; check mesh leveling results',
			move_gcode = 'G1 Z60 Y210 F6000',
			enable_preheat = True,
			selected_profile = "",
			selected_view = "raw",
			view_type = "table"
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/PrusaLevelingGuide.js"],
			css=["css/PrusaLevelingGuide.css"],
			less=["less/PrusaLevelingGuide.less"],
			photo_heatbed=["img/photo_headbed.png"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			PrusaLevelingGuide=dict(
				displayName="Prusa Leveling Guide Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="scottrini",
				repo="OctoPrint-PrusaLevelingGuide",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/scottrini/OctoPrint-PrusaLevelingGuide/archive/{target_version}.zip"
			)
		)

	##~~ GCode Received hook
	
	mesh_level_responses = []
	bed_variance = None
	relative_values = []
	last_result = None
	regex = re.compile(r"^(  -?\d+.\d+)+$")
	waiting_for_response = False
	sent_time = False
	
	def mesh_level_generate(self):
		
		mesh_values = []
		
		for response in self.mesh_level_responses:
			response = re.sub(r"^[ ]+", "", response)
			response = re.sub(r"[ ]+", ",", response)
			for i in response.split(","):
				mesh_values.append(float(i))
		
		self.bed_variance = round(max(mesh_values) - min(mesh_values), 3)

		center = mesh_values[24]
		
		self.relative_values = [mesh_values[x] - center for x in [0,3,6,21,24,27,42,45,48]]
		self.last_result = time.mktime(datetime.datetime.now().timetuple())
		del self.mesh_level_responses[:]
		
		

	def check_for_mesh_response(self, comm_instance, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
		if gcode == "G81" or gcode == "G29":
			self.waiting_for_response = True
			self.sent_time = time.time()
			del self.mesh_values[:]

	def mesh_level_check(self, comm, line, *args, **kwargs):
		if not hasattr(self, 'waiting_for_response') or not self.waiting_for_response == True:
			return line
		
		if (time.time() - self.sent_time) > 100:
			self.waiting_for_response = False
			return line

		if self.regex.match(line.rstrip()):
			self.mesh_level_responses.append(line)
			if len(self.mesh_level_responses) == 7:
				self.mesh_level_generate()
		return line
	
			

__plugin_name__ = "Prusa Leveling Guide"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PrusaLevelingGuidePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
				"octoprint.comm.protocol.gcode.received": __plugin_implementation__.mesh_level_check,
				"octoprint.comm.protocol.gcode.sent": __plugin_implementation__.check_for_mesh_response
	}

