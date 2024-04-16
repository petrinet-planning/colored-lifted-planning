from .variable import Variable
from translation.type_node import TypeNode

class GuardExpression:
    def __init__(self, op=None, left=None, right=None, value=None):
        self.op = op
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self) -> str:
        if isinstance(self.value, Variable):
            return self.value.display_name
        elif self.value:
            return f"{self.value}"
        elif self.op == "!":
            return f"{self.op}{self.left}"
        else:
            return f"({self.left} {self.op} {self.right})"
        
    #This method is only for generating the type guards for the transitions. These are of the form "x eq l0 or x eq l1 or x eq l2"
    def build_guard(type: TypeNode, variable):
        
        return GuardExpression(op="and", left = GuardExpression(op="gte", left=GuardExpression(value=variable), right=GuardExpression(value=type.first_object)), right=GuardExpression(op="lte", left=GuardExpression(value=variable), right=GuardExpression(value=type.last_object)))


        

    def generate_pnml(self):
        return f""" <condition>
                        <text>{self}</text>
                        <structure>
                            {self.generate_pnml_structure()}
                        </structure>
                    </condition>
                """

    def generate_pnml_structure(self):
        if isinstance(self.value, Variable):
            return f"<variable refvariable=\"{self.value.strValue}\"/>"
        
        if self.value:
            return f"<useroperator declaration=\"{self.value}\"/>"
        
        elif self.op == "!":
            return f""" <not>
                            <subterm>
                                {self.left.generate_pnml_structure()}
                            </subterm>
                        </not>"""
        
        elif self.op == "eq":
            return f""" <subterm>
                            <equality>
                                <subterm>
                                    {self.left.generate_pnml_structure()}
                                </subterm>
                                <subterm>
                                    {self.right.generate_pnml_structure()}
                                </subterm>
                            </equality>
                        </subterm>"""
        
        elif self.op == "gte":
            return f""" <subterm>
                            <greaterthanorequal>
                                <subterm>
                                    {self.left.generate_pnml_structure()}
                                </subterm>
                                <subterm>
                                    {self.right.generate_pnml_structure()}
                                </subterm>
                            </greaterthanorequal>
                        </subterm>"""
        
        elif self.op == "lte":
            return f""" <subterm>
                            <lessthanorequal>
                                <subterm>
                                    {self.left.generate_pnml_structure()}
                                </subterm>
                                <subterm>
                                    {self.right.generate_pnml_structure()}
                                </subterm>
                            </lessthanorequal>
                        </subterm>"""

        else:
            return f"""<{self.op}>
                            <subterm>
                                {self.left.generate_pnml_structure()}
                            </subterm>
                            <subterm>
                                {self.right.generate_pnml_structure()}
                            </subterm>
                        </{self.op}>"""
        
    """
     <condition>
                    <text>((l gte l0 and l lte l2) and (p gte p0 and p lte p0))</text>
                    <structure>
                        <and>
                            <subterm>
                                <and>
                                    <subterm>
                                        <greaterthanorequal>
                                            <subterm>
                                                <variable refvariable="Varl"/>
                                            </subterm>
                                            <subterm>
                                                <useroperator declaration="l0"/>
                                            </subterm>
                                        </greaterthanorequal>
                                    </subterm>
                                    <subterm>
                                        <lessthanorequal>
                                            <subterm>
                                                <variable refvariable="Varl"/>
                                            </subterm>
                                            <subterm>
                                                <useroperator declaration="l2"/>
                                            </subterm>
                                        </lessthanorequal>
                                    </subterm>
                                </and>
                            </subterm>
                            <subterm>
                                <and>
                                    <subterm>
                                        <greaterthanorequal>
                                            <subterm>
                                                <variable refvariable="Varp"/>
                                            </subterm>
                                            <subterm>
                                                <useroperator declaration="p0"/>
                                            </subterm>
                                        </greaterthanorequal>
                                    </subterm>
                                    <subterm>
                                        <lessthanorequal>
                                            <subterm>
                                                <variable refvariable="Varp"/>
                                            </subterm>
                                            <subterm>
                                                <useroperator declaration="p0"/>
                                            </subterm>
                                        </lessthanorequal>
                                    </subterm>
                                </and>
                            </subterm>
                        </and>
                    </structure>
                </condition>
    """