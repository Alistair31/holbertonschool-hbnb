import unittest
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)


def run_hbnb_tests():
    print("="*50)
    print("🚀 DÉMARRAGE DE LA SUITE DE TESTS HBNB")
    print("="*50)

    loader = unittest.TestLoader()
    # On cherche dans le dossier 'unitests'
    suite = loader.discover('unitests')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS")
    print(f"Tests lancés : {result.testsRun}")
    print(f"Succès       : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Échecs       : {len(result.failures)}")
    print(f"Erreurs      : {len(result.errors)}")
    print("="*50)

    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == "__main__":
    run_hbnb_tests()
