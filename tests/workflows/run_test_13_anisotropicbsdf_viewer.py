import os

from ansys_optical_automation.interop_process.BSDF_converter import BsdfStructure


def unittest_planesymmetric_brdf_zemax_run():
    """
    Test 1.

    Returns
    -------


    """
    # Test 1
    bsdf_data = BsdfStructure()
    cwd = os.path.dirname(os.path.realpath(__file__))
    bsdf_data.filename_input = os.path.join(cwd, "example_models", "test_13_planesymmetric_brdf_zemax.bsdf")
    bsdf_data.import_data(0)
    bsdf_data.write_speos_anisotropicbsdf_file()
    del bsdf_data


def unittest_planesymmetric_btdf_zemax_run():
    """
    Test 2.

    Returns
    -------


    """
    bsdf_data = BsdfStructure()
    cwd = os.path.dirname(os.path.realpath(__file__))
    bsdf_data.filename_input = os.path.join(cwd, "example_models", "test_13_planesymmetric_btdf_zemax.bsdf")
    bsdf_data.import_data(0)
    bsdf_data.write_speos_anisotropicbsdf_file()
    del bsdf_data


def unittest_asymmetrical4d_btdf_zemax_run():
    """
    Test 3.

    Returns
    -------


    """
    bsdf_data = BsdfStructure()
    cwd = os.path.dirname(os.path.realpath(__file__))
    bsdf_data.filename_input = os.path.join(cwd, "example_models", "test_13_asymmetrical4d_btdf_zemax.bsdf")
    bsdf_data.import_data(0)
    bsdf_data.write_speos_anisotropicbsdf_file()
    del bsdf_data


def unittest_brdf_one_wavelength_speos_run():
    """
    Test 4.

    Returns
    -------


    """
    bsdf_data = BsdfStructure()
    cwd = os.path.dirname(os.path.realpath(__file__))
    bsdf_data.filename_input = os.path.join(cwd, "example_models", "test_13_brdf_one_wavelength_speos.brdf")
    bsdf_data.import_data(0)
    bsdf_data.write_zemax_file(0)
    del bsdf_data


def unittest_asymmetrical4d_brdf_speoss_run():
    """
    Test 5.

    Returns
    -------


    """
    bsdf_data = BsdfStructure()
    cwd = os.path.dirname(os.path.realpath(__file__))
    bsdf_data.filename_input = os.path.join(cwd, "example_models", "test_13_asymmetrical4d_brdf_speos.anisotropicbsdf")
    bsdf_data.import_data(0)
    bsdf_data.write_zemax_file(0)
    del bsdf_data
