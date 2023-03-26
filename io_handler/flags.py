import subprocess




output = subprocess.check_output("rustc --print target-features".split())
features = output.decode("utf-8").split("\n")

feat = []

for f in features:
    if f.startswith("Code-generation") or f.startswith("Features"):
        continue

    string = "+"
    for ch, ch1 in zip(f, f[1:]): 
        if ch.isspace():
            continue
        if ch != "-":
            string += ch
        elif ch1 != " ":
            string += "-"
            string += ch1
        else:
            break
    if not string: continue
    string = string.strip()
    feat.append(string)
    if string == "+xop":
        break
        
out = ",".join(feat)
print(out)
with open ("target_features.txt", "w") as f:
    f.write(out)


