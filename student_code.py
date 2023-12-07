def ask(var, value, evidence, bn):
    # separate into two evidences 
    # in order to find var +/-
    tested_evidence = evidence.copy()
    tested_evidence[var] = value
    oppo_evidence = evidence.copy()
    oppo_evidence[var] = not value
    
    # separate variables into known and unknown 
    # in order to decide whether there is a need to 
    # calculate single possibility or +/- possibilities
    known_var = tested_evidence.keys()
    upper_joint = find_prob(bn, known_var, tested_evidence, bn.variable_names.copy())
    normal_constant = upper_joint + find_prob(bn, known_var, oppo_evidence, bn.variable_names.copy())

    return round(upper_joint/normal_constant,10)


def find_prob(bn, known_var, evidence, ttl_var):
        # if there is no more variables
        # return 1
        if not ttl_var:
             return 1
        else:
            # calculate possibility according to variable's sequency
            var = ttl_var.pop(0)
            
            # calculate single possibility for known var
            if var in known_var:
                prob = bn.variables[bn.variable_names.index(var)].probability(evidence[var],evidence)

                if len(ttl_var) == 0:
                    return prob
                if len(ttl_var) > 0:
                    joint = prob * find_prob(bn, known_var, evidence, ttl_var.copy())
                    return joint
            # calculate both possibility for unknown var
            else:
                if len(ttl_var) == 0:
                    return 1
                if len(ttl_var) > 0:
                    evidence_true = evidence.copy()
                    evidence_true[var] = True
                    evidence_false = evidence.copy()
                    evidence_false[var] = False

                    prob_true = bn.variables[bn.variable_names.index(var)].probability(evidence_true[var], evidence_true)
                    prob_false = bn.variables[bn.variable_names.index(var)].probability(evidence_false[var], evidence_false)

                    return prob_true * find_prob(bn, known_var, evidence_true, ttl_var.copy()) + \
                            prob_false * find_prob(bn, known_var, evidence_false, ttl_var.copy())
