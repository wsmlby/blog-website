import os
import shutil
from jinja2 import Environment, FileSystemLoader
import markdown2
import frontmatter

# 1. Set up paths
SRC_DIR = 'src'
STATIC_DIR = 'static'
OUTPUT_DIR = 'docs'
BLOGS_DIR = os.path.join(SRC_DIR, 'blogs')
BLOGS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'blogs')

# Clean up the output directory
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(BLOGS_OUTPUT_DIR)

# 2. Copy static files
for item in os.listdir(STATIC_DIR):
    source_item = os.path.join(STATIC_DIR, item)
    dest_item = os.path.join(OUTPUT_DIR, item)
    if os.path.isdir(source_item):
        shutil.copytree(source_item, dest_item)
    else:
        shutil.copy2(source_item, dest_item)

# 3. Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(SRC_DIR), trim_blocks=True, lstrip_blocks=True)

# 4. Process and render blog posts
posts = []
for filename in os.listdir(BLOGS_DIR):
    if filename.endswith(('.md', '.html')):
        filepath = os.path.join(BLOGS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            post_data = post.metadata
            post_data['slug'] = filename.rsplit('.', 1)[0]
            post_data['path'] = f"/blogs/{post_data['slug']}.html"
            posts.append(post_data)

            output_path = os.path.join(BLOGS_OUTPUT_DIR, f"{post_data['slug']}.html")

            if filename.endswith('.md'):
                blog_template = env.get_template('templates/blog_page.html')
                post_data['content'] = markdown2.markdown(
                    post.content,
                    extras={
                        'fenced-code-blocks': None,
                        'tables': None,
                        'html-classes': {
                            'table': 'w-full my-4 text-left border-collapse shadow-lg rounded-lg overflow-hidden',
                            'thead': 'bg-gray-700',
                            'th': 'p-3 font-bold uppercase text-white border-b border-gray-600',
                            'td': 'p-3 border-b border-gray-800',
                            'tr': 'hover:bg-gray-800'
                        }
                    }
                )
                html_content = blog_template.render(post=post_data, title=post_data['title'], page='blog')
            elif filename.endswith('.html'):
                html_template = env.from_string(post.content)
                html_content = html_template.render(post=post_data, title=post_data['title'], page='blog')

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

posts.sort(key=lambda x: x['date'], reverse=True)

# Render blog index page
blog_index_template = env.get_template('templates/blog_index.html')
html_content = blog_index_template.render(posts=posts, title="Blog", page='blog')
output_path = os.path.join(BLOGS_OUTPUT_DIR, 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

# 5. Render the homepage (index.html) with blog posts
index_template = env.get_template('index.html')
html_content = index_template.render(posts=posts, title="Home", page='index.html')
with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Site built successfully in '{OUTPUT_DIR}' directory.")
