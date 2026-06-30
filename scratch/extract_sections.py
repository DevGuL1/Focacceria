import subprocess

def main():
    content = subprocess.check_output('git show HEAD:templates/public/home.html', shell=True).decode('utf-8', errors='ignore')
    lines = content.splitlines()
    
    sections = []
    current_section = []
    in_section = False
    
    for line in lines:
        if '<section' in line:
            if in_section:
                sections.append("\n".join(current_section))
                current_section = []
            in_section = True
        if in_section:
            current_section.append(line)
            if '</section>' in line:
                sections.append("\n".join(current_section))
                current_section = []
                in_section = False
                
    if current_section:
        sections.append("\n".join(current_section))

    with open('scratch/sections.txt', 'w', encoding='utf-8') as f:
        for idx, sec in enumerate(sections):
            f.write(f"=== SECTION {idx+1} ===\n")
            f.write(sec)
            f.write("\n" + "="*50 + "\n\n")
    print("Done writing scratch/sections.txt")

if __name__ == '__main__':
    main()
