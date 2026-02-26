import os

def fix_links_rel(filepath):
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The issue might be that links are opened with an opener, which triggers Cloudflare/bot protection on the target site.
    # We can inject a tiny script that adds rel="noopener noreferrer" to all links.
    # For index.html, we inject it inside the srcdoc just before </body> or at the end of the content
    # For femet_profile.html, we inject it before </body>
    
    script_injection = "<script>document.addEventListener('DOMContentLoaded', function() { document.querySelectorAll('a').forEach(a => { a.setAttribute('target', '_blank'); a.setAttribute('rel', 'noopener noreferrer'); }); });</script>"
    
    if "</body>" in content:
        content = content.replace("</body>", f"{script_injection}</body>")
        print(f"Injected script before </body> in {filepath}")
    else:
        content += script_injection
        print(f"Appended script to {filepath}")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_links_rel('index.html')
fix_links_rel('femet_profile.html')
