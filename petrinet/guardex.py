from .variable import Variable

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
    def build_guard(objects: list[str], variable):
        if not objects:
            return None
        
        #Base case
        if len(objects) == 1:
            return GuardExpression(op="eq", left=GuardExpression(value=variable), right=GuardExpression(value=objects[0]))

        #Recursive case
        type1 = objects[0]
        type2 = objects[1]
        rest = objects[2:]

        expr_type1 = GuardExpression(op="eq", left=GuardExpression(value=variable), right=GuardExpression(value=type1))
        expr_type2 = GuardExpression(op="eq", left=GuardExpression(value=variable), right=GuardExpression(value=type2))

        combined_expr = GuardExpression(op="or", left=expr_type1, right=expr_type2)

        if rest:
            return GuardExpression(op="or", left=combined_expr, right=GuardExpression.build_guard(rest, variable))
        else:
            return combined_expr

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
                    <text>((z eq t0 and ((x eq l0 or x eq l1) or x eq l2)) and ((z eq l0 or z eq l1) or z eq l2))</text>
                    <structure>
                        <and>
                            <subterm>
                                <and>
                                    <subterm>
                                        <equality>
                                            <subterm>
                                                <variable refvariable="Varz"/>
                                            </subterm>
                                            <subterm>
                                                <useroperator declaration="t0"/>
                                            </subterm>
                                        </equality>
                                    </subterm>
                                    <subterm>
                                        <or>
                                            <subterm>
                                                <or>
                                                    <subterm>
                                                        <equality>
                                                            <subterm>
                                                                <variable refvariable="Varx"/>
                                                            </subterm>
                                                            <subterm>
                                                                <useroperator declaration="l0"/>
                                                            </subterm>
                                                        </equality>
                                                    </subterm>
                                                    <subterm>
                                                        <equality>
                                                            <subterm>
                                                                <variable refvariable="Varx"/>
                                                            </subterm>
                                                            <subterm>
                                                                <useroperator declaration="l1"/>
                                                            </subterm>
                                                        </equality>
                                                    </subterm>
                                                </or>
                                            </subterm>
                                            <subterm>
                                                <equality>
                                                    <subterm>
                                                        <variable refvariable="Varx"/>
                                                    </subterm>
                                                    <subterm>
                                                        <useroperator declaration="l2"/>
                                                    </subterm>
                                                </equality>
                                            </subterm>
                                        </or>
                                    </subterm>
                                </and>
                            </subterm>
                            <subterm>
                                <or>
                                    <subterm>
                                        <or>
                                            <subterm>
                                                <equality>
                                                    <subterm>
                                                        <variable refvariable="Varz"/>
                                                    </subterm>
                                                    <subterm>
                                                        <useroperator declaration="l0"/>
                                                    </subterm>
                                                </equality>
                                            </subterm>
                                            <subterm>
                                                <equality>
                                                    <subterm>
                                                        <variable refvariable="Varz"/>
                                                    </subterm>
                                                    <subterm>
                                                        <useroperator declaration="l1"/>
                                                    </subterm>
                                                </equality>
                                            </subterm>
                                        </or>
                                    </subterm>
                                    <subterm>
                                        <equality>
                                            <subterm>
                                                <variable refvariable="Varz"/>
                                            </subterm>
                                            <subterm>
                                                <useroperator declaration="l2"/>
                                            </subterm>
                                        </equality>
                                    </subterm>
                                </or>
                            </subterm>
                        </and>
                    </structure>
                </condition>
    """