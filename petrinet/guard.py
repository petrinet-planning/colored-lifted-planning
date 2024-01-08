# This class should be remade to be more general, right now it's only for the precondition equality guards

class Guard:
    def __init__(self, variables: tuple[str, str], notEqual: bool = False) -> None:
        self.variables = variables
        self.notEqual = notEqual

    def __str__(self):
        return self.name

    def generate_pnml(self):
        values_list = list(self.variables.values())
        var1, var2 = values_list[0], values_list[1]
        
        condition_text = f"!({var1.display_name} eq {var2.display_name})" if self.notEqual else f"({var1.display_name} eq {var2.display_name})"

        variable_structure = f"""
            <subterm>
                <equality>
                    <subterm>
                        <variable refvariable="{var1.strValue}"/>
                    </subterm>
                    <subterm>
                        <variable refvariable="{var2.strValue}"/>
                    </subterm>
                </equality>
            </subterm>
        """

        not_tag = "<not>" if self.notEqual else ""
        not_tag_end = "</not>" if self.notEqual else ""
        return f"""
            <condition>
                    <text>{condition_text}</text>
                    <structure>
                        {not_tag}
                            {variable_structure}
                        {not_tag_end}
                     </structure>
            </condition>
        """

"""
<condition>
    <text>!(x:object eq y:object)</text>
    <structure>
        <not>
            <subterm>
                <equality>
                    <subterm>
                        <variable refvariable="Varx_object"/>
                    </subterm>
                    <subterm>
                        <variable refvariable="Vary_object"/>
                    </subterm>
                </equality>
            </subterm>
        </not>
    </structure>
</condition>
"""