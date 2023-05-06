import unittest


def run_test_base_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='tests')
    runner = unittest.TextTestRunner()
    runner.run(suite)


def run_api_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='tests/api')
    runner = unittest.TextTestRunner()
    runner.run(suite)


def run_services_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='tests/services')
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    run_test_base_tests()
    run_api_tests()
    run_services_tests()
