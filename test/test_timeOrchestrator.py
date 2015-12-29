from unittest import TestCase

from mock import MagicMock

from time_orchestrator import TimeOrchestrator


class TestTimeOrchestrator(TestCase):
    def test_whenStartRequested_thenStartCalled(self):
        fake_digital_ocean_connector = MagicMock()
        orchestrator = TimeOrchestrator(fake_digital_ocean_connector)
        orchestrator.start("target")
        self.assertTrue(orchestrator.started)
        self.assertFalse(orchestrator.stop_requested)
        fake_digital_ocean_connector.start.assert_called_once_with('target')

    def test_whenStartRequestedTwice_thenStartCalledOnce(self):
        fake_digital_ocean_connector = MagicMock()
        orchestrator = TimeOrchestrator(fake_digital_ocean_connector)
        orchestrator.start("target")
        orchestrator.start("target")
        self.assertTrue(orchestrator.started)
        self.assertFalse(orchestrator.stop_requested)
        fake_digital_ocean_connector.start.assert_called_once_with('target')

    def test_whenStartAndStopRequested_thenStartCalledOnceAndStopScheduled(self):
        fake_digital_ocean_connector = MagicMock()
        orchestrator = TimeOrchestrator(fake_digital_ocean_connector)
        orchestrator.start("target")
        orchestrator.stop("target")
        self.assertTrue(orchestrator.started)
        self.assertTrue(orchestrator.stop_requested)
        fake_digital_ocean_connector.start.assert_called_once_with('target')
