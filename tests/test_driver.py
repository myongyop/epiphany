#!/usr/bin/env python3
"""
USB Microscope Driver Tests
"""

import unittest
import sys
import os

# Import driver module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from driver.microscope_driver import MicroscopeDriver

class TestMicroscopeDriver(unittest.TestCase):
    """Microscope driver test class"""
    
    def setUp(self):
        """Test setup"""
        self.driver = MicroscopeDriver()
    
    def tearDown(self):
        """Test cleanup"""
        if self.driver.is_connected:
            self.driver.disconnect()
    
    def test_driver_initialization(self):
        """Driver initialization test"""
        self.assertIsNotNone(self.driver)
        self.assertFalse(self.driver.is_connected)
        self.assertIsNone(self.driver.device)
    
    def test_device_info_empty(self):
        """Device info test when not connected"""
        info = self.driver.get_device_info()
        self.assertEqual(info, {})
    
    def test_brightness_validation(self):
        """LED brightness validation test"""
        # Should return False when not connected
        self.assertFalse(self.driver.set_led_brightness(128))
        
        # Invalid range test
        self.assertFalse(self.driver.set_led_brightness(-1))
        self.assertFalse(self.driver.set_led_brightness(256))
    
    def test_control_command_without_connection(self):
        """Control command test when not connected"""
        result = self.driver.send_control_command(0x01, 128)
        self.assertFalse(result)
    
    def test_capture_frame_without_connection(self):
        """Frame capture test when not connected"""
        frame = self.driver.capture_frame()
        self.assertIsNone(frame)

class TestUSBScanner(unittest.TestCase):
    """USB scanner test class"""
    
    def test_scanner_import(self):
        """USB scanner module import test"""
        try:
            sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))
            import usb_scanner
            self.assertTrue(True)
        except ImportError:
            self.fail("Cannot import USB scanner module")

def run_tests():
    """Run tests"""
    print("Starting USB microscope driver tests...")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestMicroscopeDriver))
    suite.addTests(loader.loadTestsFromTestCase(TestUSBScanner))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)