import nmap
import openai

openai.api_key = "__API__KEY__"
model_engine = "text-davinci-003"
nm = nmap.PortScanner()


def scanner(ip: str, profile: int) -> str:
    profile_argument = ""
    # The port profiles or scan types user can choose
    if profile == 1:
        profile_argument = '-Pn -sV -T4 -O -F'
    elif profile == 2: 
        profile_argument = '-Pn -T4 -A -v'
    elif profile == 3:
        profile_argument = '-Pn -sS -sU -T4 -A -v'
    elif profile == 4:
        profile_argument = '-Pn -p- -T4 -A -v'
    elif profile == 5:
        profile_argument = '-Pn -sS -sU -T4 -A -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script=vuln'
    else:
        raise ValueError(f"Invalid Argument: {profile}")
    # The scanner with GPT Implemented
    nm.scan('{}'.format(ip), arguments='{}'.format(profile_argument))
    json_data = nm.analyse_nmap_xml_scan()
    analyze = json_data["scan"]
    try:
        # Prompt about what the quary is all about
        prompt = "do a vulnerability analysis of {} and return a vulnerabilty report in json".format(
            analyze)
        # A structure for the request
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
        )
        response = completion.choices[0].text
    except KeyboardInterrupt:
        print("Bye")
        quit()
    print(response)
    return 'Done'
