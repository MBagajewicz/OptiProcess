##################################################################################################################
# region Titles and Header
# Nature: Generic discrete values resolver
# Methodology: Resolve calculated discrete-value generators
##################################################################################################################
# VERSION        DATE                    AUTHOR          DESCRIPTION OF CHANGES MADE
#   0.0          03-Sep-2026             Diego Oliva     Generic calculated discrete-values resolver
##################################################################################################################
# endregion
##################################################################################################################


def resolve_calculated_discrete_values(m_d, m_p, calculated_values_generators):
    """Resolve calculated discrete values declared by generator markers."""

    discrete_values = m_d['Discrete_Values_of_Variables']
    generation_data = m_p.get('Discrete_Values_Generation', {})

    for i, values in enumerate(discrete_values):

        if not isinstance(values, str):
            continue

        if not values.startswith('Calculated_'):
            continue

        generator_name = values

        if generator_name not in generation_data:
            raise ValueError(
                f"No generation parameters found for '{generator_name}'."
            )

        parameters = generation_data[generator_name].get(
            'Parameters',
            {}
        )

        if generator_name not in calculated_values_generators:
            raise ValueError(
                f"No generator module found for '{generator_name}'."
            )

        calculations_module = calculated_values_generators[generator_name]

        if not hasattr(calculations_module, generator_name):
            raise AttributeError(
                f"Generator '{generator_name}' was not found in "
                f"module '{calculations_module.__name__}'."
            )

        generator = getattr(calculations_module, generator_name)

        discrete_values[i] = generator(
            m_p=m_p,
            parameters=parameters
        )
