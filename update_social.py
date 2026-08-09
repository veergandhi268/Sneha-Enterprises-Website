import re

css = """
        /* ─── FLOATING SOCIAL ─── */
        .floating-social {
            position: fixed;
            right: 0;
            top: 50%;
            transform: translateY(-50%);
            z-index: 999;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 12px;
        }

        .social-btn {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            height: 48px;
            width: max-content;
            padding-right: 14px;
            padding-left: 14px;
            border-top-left-radius: 50px;
            border-bottom-left-radius: 50px;
            border-top-right-radius: 0;
            border-bottom-right-radius: 0;
            text-decoration: none;
            overflow: hidden;
            transition: padding-left 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                        box-shadow 0.4s ease;
        }

        .social-btn.facebook {
            background: linear-gradient(135deg, #1877f2, #0a58ca);
            box-shadow: -4px 0 25px rgba(24, 119, 242, 0.35);
        }
        .social-btn.instagram {
            background: linear-gradient(135deg, #f58529, #dd2a7b, #8134af, #515bd4);
            box-shadow: -4px 0 25px rgba(221, 42, 123, 0.4);
        }

        .social-btn .social-icon {
            width: 20px;
            height: 20px;
            fill: #fff;
            flex-shrink: 0;
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .social-btn .social-label {
            color: #fff;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            white-space: nowrap;
            max-width: 0;
            opacity: 0;
            margin-left: 0;
            transition: max-width 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                        opacity 0.3s ease,
                        margin-left 0.4s ease;
        }

        .social-btn:hover .social-icon {
            transform: scale(1.1);
        }

        .social-btn:hover .social-label {
            max-width: 120px;
            opacity: 1;
            margin-left: 10px;
        }

        .social-btn:hover {
            padding-left: 18px;
        }
"""

def update_file(filename, is_index=False):
    with open(filename, 'r') as f:
        content = f.read()
    
    # We want to replace the whole FLOATING SOCIAL block.
    # In about.html it looks like:
    # /* ─── FLOATING SOCIAL ─── */
    # ... down to .hero or whatever is next.
    
    # For a robust replacement, let's find the start of /* ─── FLOATING SOCIAL ─── */
    # and the next comment block like /* ─── HERO SECTION
    
    m = re.search(r'/\*\s*(?:───|-+)\s*FLOATING SOCIAL.*?(?=/\*\s*(?:───|-+)|</style>)', content, re.DOTALL)
    if m:
        if is_index:
            # For index, we need to keep the .floating-social { ... opacity:0 ... visible } logic
            pass
        else:
            content = content[:m.start()] + css + content[m.end():]
            with open(filename, 'w') as f:
                f.write(content)
            print(f'Updated {filename}')
    else:
        # Fallback if no comment
        print(f'Could not find block in {filename}')

update_file('/Users/apple/SnehaEnterprises website/about.html')
update_file('/Users/apple/SnehaEnterprises website/services.html')
update_file('/Users/apple/SnehaEnterprises website/contact.html')
update_file('/Users/apple/SnehaEnterprises website/portfolio.html')
update_file('/Users/apple/SnehaEnterprises website/ai.html')
