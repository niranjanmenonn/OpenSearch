from flask import Flask, request, render_template, Response, send_file, session, redirect, url_for, jsonify
from flask_talisman import Talisman
from flask_session import Session
import requests
from bs4 import BeautifulSoup
import json
import re
import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from urllib.parse import quote_plus, urlparse
import webbrowser
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import spacy
from graphviz import Digraph
import io
import feedparser
from datetime import datetime
from googleapiclient.discovery import build
import random
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import screen_brightness_control as sbc
import subprocess
from urllib.parse import urlunparse, parse_qs
# Security configurations
def setup_encryption():   #PBKDF2HMAC + Fernet Encryption
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'your-salt-here',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(b'your-password'))
    return Fernet(key)

def obfuscate_query(query):   #query obfuscation
    padding = ''.join(random.choice(' ') for _ in range(random.randint(1, 3)))
    return f"{query}{padding}"

def secure_session(session_data):   #sha.256() session privacy
    return hashlib.sha256(str(session_data).encode()).hexdigest()

def secure_api_call(endpoint, params):   #secure API calls
    headers = {'X-Disable-Logging': 'true'}
    sanitized_params = {k: v for k, v in params.items() if not k.startswith('_')}
    return requests.get(endpoint, params=sanitized_params, headers=headers)

# Initialize encryption
fernet = setup_encryption()

API_KEY = 'ENTER_YOUR_API_KEY_HERE'
SEARCH_ENGINE_ID = 'ENTER_YOUR_SEARCH_ENGINE_ID_HERE'

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

# Add urlparse filter to Jinja2
app.jinja_env.filters['urlparse'] = urlparse

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = hashlib.sha256(os.urandom(32)).hexdigest()
Session(app)

csp = {   #CSP & Security Headers
    'default-src': [
        "'self'",
        'https://apis.google.com',
        'https://cdnjs.cloudflare.com'
    ],
    'script-src': [
        "'self'",
        'https://apis.google.com',
        'https://cdnjs.cloudflare.com'
    ],
    'style-src': [
        "'self'",
        'https://cdnjs.cloudflare.com',
        "'unsafe-inline'"
    ],
    'font-src': [
        "'self'",
        'https://cdnjs.cloudflare.com'
    ],
    'img-src': [
        "'self'",
        'https://*.ytimg.com',
        'https://*.youtube.com',
        'https://*.vimeo.com',
        'https://*.dailymotion.com',
        'https://*.googleusercontent.com',
        'https://*.ggpht.com',
        'data:',
        '*'
    ]
}
Talisman(app, content_security_policy=csp)
def get_category_news(category=None):
    news_sources = {
        'technology': [
            'https://feeds.feedburner.com/ndtvgadgets-latest',
            'https://timesofindia.indiatimes.com/rssfeeds/66949542.cms',
            'https://www.techradar.com/rss'
        ],
        'business': [
            'https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms',
            'https://feeds.feedburner.com/ndtvprofit-latest'
        ],
        'world': [
            'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms',
            'https://feeds.feedburner.com/ndtvnews-world-news'
        ],
        'india': [
            'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms',
            'https://feeds.feedburner.com/ndtvnews-india-news'
        ],
        'top_stories': [
            'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
            'https://feeds.feedburner.com/ndtvnews-top-stories',
            'https://www.thehindu.com/news/feeder/default.rss',
            'https://www.indiatoday.in/rss/1206514',
            'https://economictimes.indiatimes.com/rssfeedstopstories.cms'
        ]
    }

    def parse_date(date_str):
        date_formats = [
            '%a, %d %b %Y %H:%M:%S %z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%S+%H:%M',
            '%a, %d %b %Y %H:%M:%S GMT',
            '%Y-%m-%d %H:%M:%S'
        ]
        
        if 'T' in date_str and '+' in date_str:
            date_str = date_str.replace('+05:30', '+0530')
        
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                continue
        
        return datetime.now()
    
    sources_to_use = news_sources.get(category, news_sources['top_stories']) if category else news_sources['top_stories']
    
    all_news = []
    for url in sources_to_use:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                image_url = None
                if 'media_content' in entry:
                    image_url = entry.media_content[0]['url']
                elif 'media_thumbnail' in entry:
                    image_url = entry.media_thumbnail[0]['url']
                elif 'links' in entry:
                    for link in entry.links:
                        if link.get('type', '').startswith('image/'):
                            image_url = link.href
                            break

                news_item = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published,
                    'summary': entry.summary if 'summary' in entry else '',
                    'source': urlparse(url).netloc.replace('www.', '').split('.')[0].title(),
                    'image_url': image_url,
                    'parsed_date': parse_date(entry.published)
                }
                all_news.append(news_item)
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            continue
    
    sorted_news = sorted(all_news, key=lambda x: x['parsed_date'], reverse=True)
    return sorted_news[:30]
def create_concept_map(query, search_results):
    try:
        graph = Digraph(comment='Concept Map', format='png')
        graph.attr(rankdir='TB', ranksep='0.8')
        graph.attr('node', 
                  shape='box',
                  style='rounded,filled',
                  fontname='Arial',
                  height='0.4',
                  width='0.4')
        
        # Create central query node
        graph.node('query', query, fillcolor='#E8F5E9', style='filled')
        
        # Fast concept extraction
        concepts = {}
        MAX_CONCEPTS = 8  # Reduced for faster generation
        
        # Process only first few results for speed
        for result in search_results[:5]:  # Limit to first 5 results
            try:
                text = fernet.decrypt(result['snippet'].encode()).decode()
                doc = nlp(text)
                
                # Quick entity extraction
                for ent in doc.ents:
                    if ent.label_ in ['PERSON', 'ORG', 'GPE', 'PRODUCT']:
                        key = (ent.text.strip(), ent.label_)
                        concepts[key] = concepts.get(key, 0) + 2
                
                # Fast noun chunk processing
                for chunk in doc.noun_chunks:
                    if len(chunk.text.split()) <= 2:  # Stricter length limit
                        key = (chunk.text.strip(), 'CONCEPT')
                        concepts[key] = concepts.get(key, 0) + 1
                        
            except Exception as e:
                continue
        
        if not concepts:
            return None
        
        # Quick sort for top concepts
        top_concepts = sorted(concepts.items(), key=lambda x: x[1], reverse=True)[:MAX_CONCEPTS]
        
        # Simplified color scheme
        colors = {
            'PERSON': '#E3F2FD',
            'ORG': '#FFF3E0',
            'GPE': '#F3E5F5',
            'PRODUCT': '#E8F5E9',
            'CONCEPT': '#FAFAFA'
        }
        
        # Fast node addition
        for (concept, type_), freq in top_concepts:
            node_id = re.sub(r'\W+', '_', concept.lower())
            graph.node(node_id, 
                      concept,
                      fillcolor=colors.get(type_, '#FFFFFF'))
            
            # Simple edge connection
            graph.edge('query', node_id)
        
        # Generate with optimized settings
        os.makedirs('static', exist_ok=True)
        graph.attr(dpi='150')  # Lower DPI for faster rendering
        graph.render('static/concept_map', cleanup=True)
        
        return 'concept_map.png' if os.path.exists('static/concept_map.png') else None
        
    except Exception as e:
        print(f"Error in create_concept_map: {e}")
        return None

def generate_leo_style_summary(snippets, query):
    cleaned_snippets = []
    for snippet in snippets:
        if len(snippet) > 20:
            clean_text = re.sub(r'(no description available|advertisement|\d+\s*cm)', '', snippet, flags=re.IGNORECASE)
            if clean_text.strip():
                cleaned_snippets.append(clean_text)

    doc = nlp(' '.join(cleaned_snippets))
    
    main_concepts = defaultdict(list)
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ['nsubj', 'dobj'] and not token.is_stop:
                main_concepts[token.head.text].append(token.text)

    summary_parts = []
    
    query_terms = query.lower().split()
    context_sentences = []
    for sent in doc.sents:
        if any(term in sent.text.lower() for term in query_terms):
            context_sentences.append(sent.text)
    
    if context_sentences:
        summary_parts.extend(context_sentences[:2])
    
    for verb, related_terms in main_concepts.items():
        if len(related_terms) >= 2:
            summary_parts.append(f"{' and '.join(related_terms)} {verb}")

    final_summary = ' '.join(summary_parts)
    final_summary = re.sub(r'\s+', ' ', final_summary).strip()
    final_summary = final_summary.replace(' .', '.').replace(' ,', ',')

    return final_summary
def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def extract_topics(text):
    doc = nlp(text)
    topics = []
    for chunk in doc.noun_chunks:
        if not chunk.root.is_stop and len(chunk.text.split()) <= 3:
            topics.append(chunk.text)
    return list(set(topics[:5]))

def clean_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    cleaned_params = {key: value for key, value in query_params.items() if not key.startswith('utm_')}
    cleaned_url = parsed_url._replace(query='&'.join([f"{key}={','.join(value)}" for key, value in cleaned_params.items()]))
    return urlunparse(cleaned_url)

def search(query):
    print(f"\nStarting search for query: {query}")
    service = build('customsearch', 'v1', developerKey=API_KEY)
    
    try:
        # Apply query obfuscation
        obfuscated_query = obfuscate_query(query)
        
        # Get regular search results
        web_result = service.cse().list(
            q=obfuscated_query,
            cx=SEARCH_ENGINE_ID,
            num=10
        ).execute()
        
        # Get image search results
        image_result = service.cse().list(
            q=obfuscated_query,
            cx=SEARCH_ENGINE_ID,
            num=10,
            searchType='image'
        ).execute()
        
        # Get video-specific results
        video_query = f"{obfuscated_query} video"
        video_result = service.cse().list(
            q=video_query,
            cx=SEARCH_ENGINE_ID,
            num=10,
            siteSearch="youtube.com,vimeo.com,dailymotion.com",
            siteSearchFilter="i"
        ).execute()
        
        print(f"Got {len(web_result.get('items', []))} web results and {len(image_result.get('items', []))} image results")
        
        # Process regular search results
        results = []
        for item in web_result.get('items', []):
            cleaned_link = clean_url(item['link'])
            if cleaned_link not in [r['link'] for r in results]:
                try:
                    is_video = any(site in cleaned_link.lower() for site in ['youtube.com/watch', 'vimeo.com', 'dailymotion.com'])
                    pagemap = item.get('pagemap', {})
                    thumbnail = ''
                    
                    if is_video:
                        # Try to get thumbnail from different possible locations
                        if 'videoobject' in pagemap:
                            thumbnail = pagemap['videoobject'][0].get('thumbnailurl', '')
                        elif 'cse_thumbnail' in pagemap:
                            thumbnail = pagemap['cse_thumbnail'][0].get('src', '')
                        elif 'cse_image' in pagemap:
                            thumbnail = pagemap['cse_image'][0].get('src', '')
                            
                        # YouTube specific handling
                        if 'youtube.com/watch' in cleaned_link:
                            video_id = cleaned_link.split('v=')[-1].split('&')[0]
                            thumbnail = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
                    
                    encrypted_data = {
                        'title': fernet.encrypt(item['title'].encode()).decode(),
                        'link': cleaned_link,
                        'snippet': fernet.encrypt(item['snippet'].encode()).decode(),
                        'domain': urlparse(cleaned_link).netloc,
                        'type': 'video' if is_video else 'web',
                        'thumbnail': thumbnail
                    }
                    results.append(encrypted_data)
                except Exception as encrypt_error:
                    print(f"Encryption error: {encrypt_error}")
                    continue

        # Process video-specific results
        video_results = []
        for item in video_result.get('items', []):
            try:
                cleaned_link = clean_url(item['link'])
                if cleaned_link not in [r['link'] for r in video_results]:
                    pagemap = item.get('pagemap', {})
                    thumbnail = ''
                    
                    # Try to get thumbnail from different possible locations
                    if 'videoobject' in pagemap:
                        thumbnail = pagemap['videoobject'][0].get('thumbnailurl', '')
                    elif 'cse_thumbnail' in pagemap:
                        thumbnail = pagemap['cse_thumbnail'][0].get('src', '')
                    elif 'cse_image' in pagemap:
                        thumbnail = pagemap['cse_image'][0].get('src', '')
                        
                    # YouTube specific handling
                    if 'youtube.com/watch' in cleaned_link:
                        video_id = cleaned_link.split('v=')[-1].split('&')[0]
                        thumbnail = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
                    
                    video_data = {
                        'title': fernet.encrypt(item['title'].encode()).decode(),
                        'link': cleaned_link,
                        'snippet': fernet.encrypt(item['snippet'].encode()).decode(),
                        'domain': urlparse(cleaned_link).netloc,
                        'type': 'video',
                        'thumbnail': thumbnail
                    }
                    video_results.append(video_data)
            except Exception as video_error:
                print(f"Video processing error: {video_error}")
                continue

        # Combine video results
        all_video_results = video_results + [r for r in results if r['type'] == 'video']
        # Remove duplicates based on link
        seen_links = set()
        unique_video_results = []
        for video in all_video_results:
            if video['link'] not in seen_links:
                seen_links.add(video['link'])
                unique_video_results.append(video)

        # Process image results
        image_results = []
        for item in image_result.get('items', []):
            try:
                image_data = {
                    'title': fernet.encrypt(item['title'].encode()).decode(),
                    'link': item['link'],
                    'image_url': item['link'],
                    'thumbnail': item.get('image', {}).get('thumbnailLink', ''),
                    'context_url': item['image']['contextLink'],
                    'width': item['image'].get('width', 0),
                    'height': item['image'].get('height', 0)
                }
                image_results.append(image_data)
            except Exception as img_error:
                print(f"Image processing error: {img_error}")
                continue

        # Process snippets and generate summary
        web_results = [r for r in results if r['type'] == 'web']
        all_snippets = []
        try:
            all_snippets = [fernet.decrypt(r['snippet'].encode()).decode() for r in web_results if r['snippet']]
            print(f"Successfully decrypted {len(all_snippets)} snippets")
        except Exception as decrypt_error:
            print(f"Decryption error: {decrypt_error}")
        
        summary = ""
        entities = []
        topics = []
        concept_map = None
        
        if all_snippets: 
            try:
                summary = generate_leo_style_summary(all_snippets, query)
                entities = extract_entities(summary)
                topics = extract_topics(summary)
                print(f"Generated summary with {len(entities)} entities and {len(topics)} topics")
                
                if web_results:
                    concept_map = create_concept_map(query, web_results)
                    
            except Exception as processing_error:
                print(f"Text processing error: {processing_error}")
                summary = "Error generating summary."
        else:
            print("No snippets available for processing")
            summary = "No relevant summary available."
            
        return {
            'results': web_results[:10],
            'video_results': unique_video_results[:10],
            'image_results': image_results,
            'summary': summary,
            'entities': entities,
            'key_topics': topics,
            'concept_map': concept_map
        }
        
    except Exception as e:
        import traceback
        print(f"Search error: {str(e)}")
        print("Full traceback:")
        print(traceback.format_exc())
        return {
            'results': [],
            'video_results': [],
            'image_results': [],
            'summary': f"An error occurred while searching: {str(e)}",
            'entities': [],
            'key_topics': [],
            'concept_map': None
        }
@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/search')
def search_interface():
    return render_template('index.html')

@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    query = request.form.get('query') or request.args.get('query')
    if not query:
        return redirect(url_for('search_interface'))
    # Secure session tracking
    session['search_hash'] = secure_session(query)
    return render_template('scanning.html', query=query)

@app.route('/final_results', methods=['GET', 'POST'])
def final_results():
    query = request.form.get('query') or request.args.get('query')
    if not query:
        return redirect(url_for('search_interface'))
        
    search_data = search(query)
    
    # Store the concept map in session if it was generated
    if search_data['concept_map']:
        session['concept_map'] = search_data['concept_map']
    
    # Decrypt web results
    for result in search_data['results']:
        result['title'] = fernet.decrypt(result['title'].encode()).decode()
        result['snippet'] = fernet.decrypt(result['snippet'].encode()).decode()
    
    # Decrypt video results
    for video in search_data['video_results']:
        video['title'] = fernet.decrypt(video['title'].encode()).decode()
        video['snippet'] = fernet.decrypt(video['snippet'].encode()).decode()
    
    # Decrypt image titles
    for image in search_data['image_results']:
        image['title'] = fernet.decrypt(image['title'].encode()).decode()
    
    return render_template('results.html',
                       query=query,
                       results=search_data['results'],
                       video_results=search_data['video_results'],
                       image_results=search_data['image_results'],
                       summary=search_data['summary'],
                       entities=search_data['entities'],
                       key_topics=search_data['key_topics'],
                       concept_map=search_data['concept_map'])

@app.route('/images', methods=['GET', 'POST'])
def image_results():
    query = request.form.get('query') or request.args.get('query')
    if not query:
        return redirect(url_for('search_interface'))
    
    search_data = search(query)
    
    # Decrypt image titles
    for image in search_data['image_results']:
        image['title'] = fernet.decrypt(image['title'].encode()).decode()
    
    return render_template('images.html',
                       query=query,
                       image_results=search_data['image_results'])

@app.route('/videos', methods=['GET', 'POST'])
def video_results():
    query = request.form.get('query') or request.args.get('query')
    if not query:
        return redirect(url_for('search_interface'))
    
    search_data = search(query)
    
    # Decrypt video results
    for video in search_data['video_results']:
        video['title'] = fernet.decrypt(video['title'].encode()).decode()
        video['snippet'] = fernet.decrypt(video['snippet'].encode()).decode()
    
    return render_template('videos.html',
                       query=query,
                       video_results=search_data['video_results'])

@app.route('/news')
def news_page():
    news_articles = get_category_news()
    return render_template('news.html', articles=news_articles, active_category=None)

@app.route('/news/<category>')
def category_news(category):
    news_articles = get_category_news(category.lower())
    return render_template('news.html', articles=news_articles, active_category=category.lower())

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')

@app.route('/preferences')
def preferences():
    return render_template('preferences.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/automater')
def automater():
    return render_template('automater.html')

# Eteon AI-2 Brightness and Volume Control APIs
@app.route('/api/brightness', methods=['GET'])
def get_brightness():
    try:
        current_brightness = sbc.get_brightness()
        # Handle both cases: when it returns a list or a single integer
        if isinstance(current_brightness, list):
            current_brightness = current_brightness[0]
        return jsonify({"brightness": current_brightness})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/brightness', methods=['POST'])
def set_brightness():
    data = request.json
    action = data.get('action', '').lower()
    
    try:
        current_brightness = sbc.get_brightness()
        # Handle both cases: when it returns a list or a single integer
        if isinstance(current_brightness, list):
            current_brightness = current_brightness[0]
        
        if action == 'increase':
            new_brightness = min(current_brightness + 10, 100)
            sbc.set_brightness(new_brightness)
            return jsonify({"brightness": new_brightness, "message": "Brightness increased"})
        
        elif action == 'decrease' or action == 'reduce':
            new_brightness = max(current_brightness - 10, 0)
            sbc.set_brightness(new_brightness)
            return jsonify({"brightness": new_brightness, "message": "Brightness decreased"})
        
        elif action.isdigit():
            new_brightness = max(0, min(int(action), 100))
            sbc.set_brightness(new_brightness)
            return jsonify({"brightness": new_brightness, "message": f"Brightness set to {new_brightness}%"})
        
        else:
            return jsonify({"error": "Invalid action. Use 'increase', 'decrease', 'reduce', or a number (0-100)"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/volume', methods=['GET'])
def get_volume():
    try:
        # Use a simpler PowerShell command to get volume
        result = subprocess.run(
            ["powershell", "-Command", "(Get-AudioDevice -PlaybackVolume).Volume"],
            capture_output=True, text=True
        )
        
        # Parse the volume level
        try:
            volume = int(float(result.stdout.strip()))
        except:
            volume = 50  # Default to 50 if parsing fails
        
        return jsonify({"volume": volume})
    except Exception as e:
        return jsonify({"error": str(e), "volume": 50}), 500

@app.route('/api/volume', methods=['POST'])
def set_volume():
    data = request.json
    action = data.get('action', '').lower()
    
    try:
        # Get current volume
        try:
            volume_result = subprocess.run(
                ["powershell", "-Command", "(Get-AudioDevice -PlaybackVolume).Volume"],
                capture_output=True, text=True
            )
            current_volume = int(float(volume_result.stdout.strip() or 50))
        except:
            current_volume = 50  # Default value
        
        if action == 'increase':
            new_volume = min(current_volume + 10, 100)
            # Set volume using PowerShell
            subprocess.run(
                ["powershell", "-Command", f"Set-AudioDevice -PlaybackVolume {new_volume}"],
                check=True
            )
            return jsonify({"volume": new_volume, "message": "Volume increased"})
        
        elif action == 'decrease' or action == 'reduce':
            new_volume = max(current_volume - 10, 0)
            # Set volume using PowerShell
            subprocess.run(
                ["powershell", "-Command", f"Set-AudioDevice -PlaybackVolume {new_volume}"],
                check=True
            )
            return jsonify({"volume": new_volume, "message": "Volume decreased"})
        
        elif action.isdigit():
            new_volume = max(0, min(int(action), 100))
            # Set volume directly
            subprocess.run(
                ["powershell", "-Command", f"Set-AudioDevice -PlaybackVolume {new_volume}"],
                check=True
            )
            return jsonify({"volume": new_volume, "message": f"Volume set to {new_volume}%"})
        
        else:
            return jsonify({"error": "Invalid action. Use 'increase', 'decrease', 'reduce', or a number (0-100)"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def parse_search_query(query):
    # Extract the website and search term from the query
    patterns = {
        'google': r'go to google and search for (.*)',
        'google_scholar': r'go to google scholar and search for (.*)',
        'wikipedia': r'go to wikipedia(?:\.com)? and search for (.*)',
        'youtube': r'go to youtube(?:\.com)? and search for (.*)',
        'stackoverflow': r'go to stack(?:\s)?overflow and search for (.*)',
        'github': r'go to github and search for (.*)',
        'amazon': r'go to amazon and search for (.*)',
        'reddit': r'go to reddit and search for (.*)',
        'twitter': r'go to twitter and search for (.*)',
        'linkedin': r'go to linkedin and search for (.*)',
        'quora': r'go to quora and search for (.*)',
        'jstor': r'go to jstor and search for (.*)',
        'sciencedirect': r'go to science(?:\s)?direct and search for (.*)',
        'researchgate': r'go to research(?:\s)?gate and search for (.*)',
        'britannica': r'go to britannica and search for (.*)',
        'vimeo': r'go to vimeo and search for (.*)',
        'dailymotion': r'go to dailymotion and search for (.*)',
        'ebay': r'go to ebay and search for (.*)',
        'flipkart': r'go to flipkart and search for (.*)'
    }
    
    for site, pattern in patterns.items():
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return site, match.group(1).strip()
    
    # Default to Google if no specific site is mentioned
    return 'google', query.strip()

@app.route('/automate_search', methods=['POST'])
def automate_search():
    query = request.form.get('query', '')
    site, search_term = parse_search_query(query)
    
    try:
        # Encode the search term for URL
        encoded_term = quote_plus(search_term)
        print(encoded_term) 
        
        # Define search URLs for different sites
        urls = {
            'google': f'https://www.google.com/search?q={encoded_term}',
            'google_scholar': f'https://scholar.google.com/scholar?q={encoded_term}',
            'wikipedia': f'https://www.wikipedia.org/search-redirect.php?search={encoded_term}',
            'youtube': f'https://www.youtube.com/results?search_query={encoded_term}',
            'stackoverflow': f'https://stackoverflow.com/search?q={encoded_term}&tab=relevance',
            'github': f'https://github.com/search?q={encoded_term}',
            'amazon': f'https://www.amazon.com/s?k={encoded_term}&ref=nb_sb_noss',  
            'reddit': f'https://www.reddit.com/search/?q={encoded_term}',
            'twitter': f'https://twitter.com/search?q={encoded_term}',
            'linkedin': f'https://www.linkedin.com/search/results/all/?keywords={encoded_term}',
            'quora': f'https://www.quora.com/search?q={encoded_term}',
            'jstor': f'https://www.jstor.org/action/doBasicSearch?Query={encoded_term}',
            'sciencedirect': f'https://www.sciencedirect.com/search?qs={encoded_term}&show=100&sortBy=relevance',
            'researchgate': f'https://www.researchgate.net/search/publication?q={encoded_term}',
            'britannica': f'https://www.britannica.com/search?query={encoded_term}&include_references=true',
            'vimeo': f'https://vimeo.com/search?q={encoded_term}',
            'dailymotion': f'https://www.dailymotion.com/search/{encoded_term}',
            'ebay': f'https://www.ebay.com/sch/i.html?_nkw={encoded_term}',
            'flipkart': f'https://www.flipkart.com/search?q={encoded_term}'
        }
        
        target_url = urls[site]
        
        # Special handling for sites that might show CAPTCHAs
        if site in ['amazon', 'sciencedirect', 'britannica', 'flipkart', 'stackoverflow']:
            browser = webbrowser.get()
            browser.open_new(target_url)
        else:
            webbrowser.open(target_url)
        
        # Format the site name for display
        display_site = site.replace('_', ' ').title()
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully opened search for "{search_term}" on {display_site}'
        })
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)  # Log the error
        return jsonify({
            'status': 'error',
            'message': error_message
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',  port=int(os.environ.get("PORT", 5000)
