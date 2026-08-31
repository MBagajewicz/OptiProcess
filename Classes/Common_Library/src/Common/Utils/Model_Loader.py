#region Titles and Header
# Nature: Call specfic model dictionary in generic code structure
# Methodology: Class to call model dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          31-Aug-2026     Diego Oliva               Proposed to call dictionary from Model definitions
##################################################################################################################
#endregion

import importlib


class Model_Loader:
    """
    Generic dynamic loader for model definitions.

    Given a model name, dynamically imports:

        <Model>.Model.Model_Def_<Model>

    and retrieves:

        Model_<Model>
    """

    @staticmethod
    def load(model_name):
        """
        Load and return the model definition.

        Parameters
        ----------
        model_name : str
            Name of the model.

        Returns
        -------
        object
            Model_<model_name>

        Example
        -------
        Model_Loader.load('STHE_1')

        dynamically loads:

            STHE_1.Model.Model_Def_STHE_1

        and returns:

            Model_STHE_1
        """

        # ---------------------------------------------------------------------
        # Validate model name
        # ---------------------------------------------------------------------

        if not model_name:
            raise ValueError(
                "Model name cannot be empty."
            )

        if not isinstance(model_name, str):
            raise TypeError(
                f"Model name must be a string. "
                f"Received: {type(model_name).__name__}"
            )

        # ---------------------------------------------------------------------
        # Build module name
        # ---------------------------------------------------------------------

        module_name = (
            f"{model_name}.Model.Model_Def_{model_name}"
        )

        # ---------------------------------------------------------------------
        # Build model object name
        # ---------------------------------------------------------------------

        object_name = f"Model_{model_name}"

        # ---------------------------------------------------------------------
        # Dynamic import
        # ---------------------------------------------------------------------

        try:

            module = importlib.import_module(module_name)

        except ImportError as e:

            raise ImportError(
                f"Could not import model definition.\n"
                f"Model  : {model_name}\n"
                f"Module : {module_name}\n"
                f"Error  : {e}"
            ) from e

        # ---------------------------------------------------------------------
        # Retrieve model definition
        # ---------------------------------------------------------------------

        if not hasattr(module, object_name):

            raise AttributeError(
                f"Model object '{object_name}' was not found in "
                f"module '{module_name}'."
            )

        return getattr(module, object_name)