import json

with open("data/projects.json", "r", encoding="utf-8") as f:
    data = json.loads(f.read())

wiki_url: str = data['wiki_url']

cf_link: str = data['curseforge']['base_url']
cf_badge: str = data['curseforge']['badge_url']

mr_link: str = data['modrinth']['base_url']
mr_badge: str = data['modrinth']['badge_url']

mods = data['projects']

table = f'<table cols="4" rows="{1 + len(mods)}">\n'
table += "<tr><td>**Name**</td><td>**CurseForge**</td><td>**Modrinth**</td><td>**GitHub**</td></tr><tbody>\n"

for mod in mods:
    name = mod['name']
    slug = mod['slug']
    if "mr_id" in mod:
        if type(slug) == str:
            cf_url = f"[![]({cf_badge.format(mod['cf_id'])})]({cf_link + slug})"
            mr_url = f"[![]({mr_badge.format(mod['mr_id'])})]({mr_link + slug})"
            wiki = wiki_url + slug
        else:
            cf_url = f"[![]({cf_badge.format(mod['cf_id'])})]({cf_link + slug['cf']})"
            mr_url = f"[![]({mr_badge.format(mod['mr_id'])})]({mr_link + slug['mr']})"
            wiki = wiki_url + slug['cf']
    else:
        cf_url = f"[![]({cf_badge.format(mod['cf_id'])})]({cf_link + slug})"
        mr_url = "Not available"
        wiki = wiki_url + slug

    if "wiki_url" in mod:
        wiki = mod['wiki_url']
    github = f"[Link]({mod['github']})" if "github" in mod else "Not available"
    table += f'<tr class="mx-wiki-search-row" data-search-text="{name}"><td>[{name}]({wiki})</td><td>{cf_url}</td><td>{mr_url}</td><td>{github}</td></tr>\n'

table += '</tbody></table>\n'

with open("docs/index.md", "r", encoding="utf-8") as f:
    content = f.read()

new_content = content.format(**{
    'table': table,
    'search': '<div style="float:right;"><form name="unused"><input id="mx-mods-table-search-input" type="text" class="mx-wiki-input" placeholder="Search"></form></div>',
    'header': '<script src="scripts/table_search.js" type="application/javascript"></script>\n<link rel="stylesheet" href="style.css">'
})

with open("docs/index.md", "w", encoding="utf-8") as f:
    f.write(new_content)
