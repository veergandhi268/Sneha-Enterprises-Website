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

        .social-btn.facebook, .social-btn.fb {
            background: linear-gradient(135deg, #1877f2, #0a58ca);
            box-shadow: -4px 0 25px rgba(24, 119, 242, 0.35);
        }
        .social-btn.instagram, .social-btn.ig {
            background: linear-gradient(135deg, #f58529, #dd2a7b, #8134af, #515bd4);
            box-shadow: -4px 0 25px rgba(221, 42, 123, 0.4);
        }

        .social-btn .social-icon, .social-btn img, .social-btn svg {
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

        .social-btn:hover .social-icon, .social-btn:hover img, .social-btn:hover svg {
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

def update_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # We find .floating-social and remove rules up to the next non-floating-social rule block or comment
    m1 = re.search(r'\.floating-social\s*\{', content)
    if not m1:
        return
        
    start_idx = m1.start()
    
    # find where this section ends. 
    # Usually it's followed by another major comment like /* or another class that isn't .social-
    
    # Let's find the first rule AFTER the .social- ones
    # We can match all `.floating-social` and `.social-*` rules
    end_idx = start_idx
    while True:
        # Match next rule
        m2 = re.search(r'([^{]+)\s*\{[^}]+\}', content[end_idx:])
        if m2:
            selector = m2.group(1).strip()
            # If the selector is a comment, skip it
            if selector.startswith('/*'):
                pass
            if 'floating-social' in selector or 'social-' in selector or '@keyframes sp' in selector:
                end_idx += m2.end()
            else:
                break
        else:
            break
            
    if end_idx > start_idx:
        # Check if there is a comment just before start_idx
        comment_match = re.search(r'/\*.*?\*/\s*$', content[:start_idx], re.DOTALL)
        if comment_match:
            start_idx = comment_match.start()
            
        new_content = content[:start_idx] + css + content[end_idx:]
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f'Updated {filename}')

update_file('/Users/apple/SnehaEnterprises website/services.html')
update_file('/Users/apple/SnehaEnterprises website/portfolio.html')
update_file('/Users/apple/SnehaEnterprises website/ai.html')
