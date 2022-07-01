# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json
import importlib.util

from ovos_plugin_manager.skills import find_skill_plugins
from neon_utils.skills.neon_skill import NeonSkill
from adapt.intent import IntentBuilder
from os import listdir, path

from mycroft.skills import skill_api_method, intent_handler


class AboutSkill(NeonSkill):
    def __init__(self):
        super(AboutSkill, self).__init__(name="AboutSkill")
        self.skill_info = None
        self._update_skills_data()

    def initialize(self):
        # TODO: Reload skills list when skills are added/removed DM
        self.bus.once("mycroft.ready", self._update_skills_data)

    @intent_handler(IntentBuilder("license_intent")
                    .require("tell").require("license")
                    .optionally("long"))
    def read_license(self, message):
        """
        Reads back the NeonAI license from skill dialog
        :param message: Message associated with request
        """
        if self.neon_in_request(message):
            if message.data.get("long"):
                self.speak_dialog("license_long")
            else:
                self.speak_dialog("license_short")

    @intent_handler(IntentBuilder("list_skills_intent")
                    .optionally("tell").require("skills"))
    def list_skills(self, message):
        """
        Lists all installed skills by name.
        :param message: Message associated with request
        """
        if self.neon_in_request(message):
            skills_list = [s['title'] for s in self.skill_info if s.get('title')]
            skills_list.sort()
            skills_to_speak = ", ".join(skills_list)
            self.speak_dialog("skills_list", data={"list": skills_to_speak})

    @skill_api_method
    def skill_info_examples(self) -> list:
        """
        API Method to build a list of examples as listed in skill metadata.
        """
        examples = [d.get('examples') or list() for d in self.skill_info]
        flat_list = [item for sublist in examples for item in sublist]
        return flat_list

    def _update_skills_data(self):
        """
        Loads skill metadata for all installed skills.
        """
        skills = list()
        skills_dirs = self.config_core["skills"].get("extra_directories") or []
        for skills_dir in skills_dirs:
            for skill in listdir(skills_dir):
                if path.isdir(path.join(skills_dir, skill)) and \
                        path.isfile(path.join(skills_dir, skill,
                                              "__init__.py")):
                    skills.append(self._load_skill_json(path.join(skills_dir,
                                                                  skill)))
        plugin_data = self._get_plugin_skill_data()
        self.skill_info = list(set(skills + plugin_data))

    def _get_plugin_skill_data(self) -> list:
        """
        Get a list of dict skill specs for all pip installed skills
        """
        skills = list()
        plugins = find_skill_plugins()
        for skill_class in plugins.values():
            skill_dir = path.dirname(importlib.util.find_spec(
                skill_class.__module__).origin)
            skills.append(self._load_skill_json(skill_dir))
        return skills

    @staticmethod
    def _load_skill_json(skill_dir: str) -> dict:
        """
        Get a dict representation of the specified skill (directory)
        :param skill_dir: directory containing skill files
        :returns: dict spec read from `skill.json` or built from skill dirname
        """
        if not path.isdir(skill_dir):
            raise FileNotFoundError(f"{skill_dir} is not a valid directory")
        if path.isfile(path.join(skill_dir, "skill.json")):
            with open(path.join(skill_dir, "skill.json")) as f:
                skill_data = json.load(f)
        else:
            skill_name = str(path.basename(skill_dir).split('.')[0]).\
                replace('-', ' ').lower()
            skill_data = {"title": skill_name}
        return skill_data

    def stop(self):
        pass


def create_skill():
    return AboutSkill()
