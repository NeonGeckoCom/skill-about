# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
#
# Copyright 2008-2021 Neongecko.com Inc. | All Rights Reserved
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
# US Patents 2008-2021: US7424516, US20140161250, US20140177813, US8638908, US8068604, US8553852, US10530923, US10530924
# China Patent: CN102017585  -  Europe Patent: EU2156652  -  Patents Pending

import pytest

from ovos_bus_client.message import Message
from neon_minerva.tests.skill_unit_test_base import SkillTestCase


class TestSkillMethods(SkillTestCase):
    def test_00_skill_init(self):
        # Test any parameters expected to be set in init or initialize methods
        from neon_utils.skills import NeonSkill

        self.assertIsInstance(self.skill, NeonSkill)
        self.assertIsInstance(self.skill.skill_info, list)

    def test_read_license(self):
        valid_message = Message("test_message",
                                {"tell": "tell", "license": "license"},
                                {"neon_should_respond": True})
        valid_message_long = Message("test_message",
                                     {"tell": "tell", "license": "license",
                                      "long": "long"},
                                     {"neon_should_respond": True})

        self.skill.read_license(valid_message)
        self.skill.speak_dialog.assert_called_with("license_short")

        self.skill.read_license(valid_message_long)
        self.skill.speak_dialog.assert_called_with("license_long")

    def test_list_skills(self):
        valid_message = Message("test_message",
                                {"tell": "tell", "skills": "skills"},
                                {"neon_should_respond": True})
        self.skill.list_skills(valid_message)
        self.skill.speak_dialog.assert_called_once()
        args = self.skill.speak_dialog.call_args
        self.assertEqual(args[0][0], "skills_list")
        self.assertEqual(list(args[1]['data'].keys())[0], "list")

    def test_skill_info_examples(self):
        examples = self.skill.skill_info_examples()
        print(examples)
        self.assertIsInstance(examples, list)
        self.assertTrue(all([isinstance(i, str) for i in examples]), examples)

    def test_update_skills_data(self):
        self.skill.skill_info = None
        self.skill._update_skills_data()
        self.assertIsInstance(self.skill.skill_info, list)
        self.assertTrue(all([isinstance(i, dict)
                             for i in self.skill.skill_info]))


if __name__ == '__main__':
    pytest.main()
