if len(sys.argv) < 2:
    print("Usage: python script.py <html_file> [output_html_file]")
    exit(1)

with open(sys.argv[1], "r") as f:
    html_content = f.read()

cd = CaseDetails(html_content)
wat / cd.case
if len(sys.argv) == 3:
    with open(sys.argv[2], "w") as f:
        f.write(str(cd.html))
