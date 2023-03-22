from combidata import Process
from combidata.classes.combination import Combination


def check(combination: Combination):
    if "received" not in combination.cache:
        return True
    result = {}
    body = combination.cache["received"]
    for key, case in combination.cache["cases"].items():
        if key not in body and not case.is_presented:
            continue
        elif not (key in body and case.gen_func(case.value, body[key])):
            combination.cache.update({"result": case.additional_fields["error"]})
            return True
        elif "change" in case.additional_fields:
            result.update({case.additional_fields["change"]: body[key]})
        elif key in result:
            continue
        else:
            result.update({key: body[key]})
    combination.cache.update({"result": result})
    return True


CHECK = Process("CHECK", check)

def form_cases(combination: Combination):
    combination.cache.update({"cases": {key: combination.init_lib[key][value] for key, value in combination.test_seed.items()}})
    return True

FORM_CASES = Process("FORM_CASES", form_cases)
