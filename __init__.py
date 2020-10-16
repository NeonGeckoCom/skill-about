# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
#
# Copyright 2008-2020 Neongecko.com Inc. | All Rights Reserved
#
# Notice of License - Duplicating this Notice of License near the start of any file containing
# a derivative of this software is a condition of license for this software.
# Friendly Licensing:
# No charge, open source royalty free use of the Neon AI software source and object is offered for
# educational users, noncommercial enthusiasts, Public Benefit Corporations (and LLCs) and
# Social Purpose Corporations (and LLCs). Developers can contact developers@neon.ai
# For commercial licensing, distribution of derivative works or redistribution please contact licenses@neon.ai
# Distributed on an "AS IS” basis without warranties or conditions of any kind, either express or implied.
# Trademarks of Neongecko: Neon AI(TM), Neon Assist (TM), Neon Communicator(TM), Klat(TM)
# Authors: Guy Daniels, Daniel McKnight, Regina Bloomstine, Elon Gasper, Richard Leeds
#
# Specialized conversational reconveyance options from Conversation Processing Intelligence Corp.
# US Patents 2008-2020: US7424516, US20140161250, US20140177813, US8638908, US8068604, US8553852, US10530923, US10530924
# China Patent: CN102017585  -  Europe Patent: EU2156652  -  Patents Pending

from mycroft.skills import MycroftSkill
from mycroft.util.log import LOG
from adapt.intent import IntentBuilder
from os import listdir, path


class AboutSkill(MycroftSkill):
    def __init__(self):
        super(AboutSkill, self).__init__(name="AboutSkill")

    def initialize(self):
        license_intent = IntentBuilder("license_intent").\
            optionally("Neon").optionally("Long").require("Tell").require("License").build()
        self.register_intent(license_intent, self.read_license)

        list_skills_intent = IntentBuilder("list_skills_intent").optionally("Neon").optionally("Tell").\
            require("Skills").build()
        self.register_intent(list_skills_intent, self.list_skills)

    def read_license(self, message):
        if self.neon_in_request(message):
            if message.data.get("Long"):
                self.speak_dialog("license_long")
            else:
                self.speak_dialog("license_short")

    def list_skills(self, message):
        if self.neon_in_request(message):
            skills_list = []
            LOG.debug("DM: List skills called")
            for skill in listdir(self.configuration_available["dirVars"]["skillsDir"]):
                LOG.debug(f"DM: {skill}")
                if path.isdir(f'{self.configuration_available["dirVars"]["skillsDir"]}/{skill}'):
                    skill_name = str(path.basename(skill).split('.')[0]).replace('-', ' ').lower()
                    LOG.debug(f"DM: {skill_name}")
                    skills_list.append(skill_name)
            skills_list.remove('')
            skills_list.sort()
            skills_to_speak = ", ".join(skills_list)
            LOG.debug(f"DM: {skills_to_speak}")
            self.speak_dialog("skills_list", data={"list": skills_to_speak})

    def stop(self):
        pass


def create_skill():
    return AboutSkill()
