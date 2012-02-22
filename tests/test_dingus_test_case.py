from nose.tools import assert_raises

from tests import test_case_fixture as module
from tests.test_case_fixture import ClassUnderTest, Collaborator

from dingus import DingusTestCase, Dingus
import dingus


class WhenObjectIsExcludedFromTest:
    def setup(self):
        class TestCase(DingusTestCase(module.ClassUnderTest,
                                      exclude=['Collaborator'])):
            pass
        self.test_case_instance = TestCase()
        self.test_case_instance.setup()

    def should_not_replace_it_with_dingus(self):
        assert module.Collaborator is Collaborator

    def should_not_allow_strings_used_to_exclude(self):
        assert_raises(ValueError,
                      DingusTestCase,
                      module.ClassUnderTest,
                      exclude='a_string')

    def teardown(self):
        self.test_case_instance.teardown()


class WhenCallingSetupFunction:
    def setup(self):
        class TestCase(DingusTestCase(module.ClassUnderTest)):
            pass
        self.test_case_instance = TestCase()
        self.test_case_instance.setup()

    def teardown(self):
        self.test_case_instance.teardown()

    def should_not_replace_module_dunder_attributes(self):
        assert isinstance(module.__name__, str)
        assert isinstance(module.__file__, str)

    def should_replace_module_non_dunder_attributes(self):
        assert isinstance(module.atomic_value, Dingus)

    def should_replace_collaborating_classes(self):
        assert isinstance(module.Collaborator, Dingus)

    def should_leave_class_under_test_intact(self):
        assert module.ClassUnderTest is ClassUnderTest


class WhenCallingTeardownFunction:
    def setup(self):
        self.original_module_dict = module.__dict__.copy()
        class TestCase(DingusTestCase(module.ClassUnderTest)):
            pass
        test_case_object = TestCase()
        test_case_object.setup()
        test_case_object.teardown()

    def should_restore_module_attributes(self):
        assert module.atomic_value is 'foo'

    def should_leave_globals_as_they_were_before_dingusing(self):
        assert module.__dict__ == self.original_module_dict


class WhenCustomTestCaseBase:
    def setup(self):
        class CustomTestBase(dingus.TestCase):
            """
            This TestBase enables setup/teardown in py.test tests
            """
            def setup_method(self, method):
                self.setup()

            def teardown_method(self, method):
                self.teardown()

        class TestCase(DingusTestCase(module.ClassUnderTest,
                base=CustomTestBase)):
            pass
        self.test_case_instance = TestCase()
        self.test_case_instance.setup()

    def teardown(self):
        self.test_case_instance.teardown()

    def test_case_should_have_setup_method_method(self):
        assert hasattr(self.test_case_instance, 'setup_method')
