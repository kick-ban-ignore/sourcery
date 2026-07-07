"""
Custom CSS for the Sourcery app - adds hover effect to the bird emoji
"""

def get_bird_css():
    return """
    <style>
    .bird-container {
        position: relative;
        display: inline-block;
        height: 5rem; /* Fixed height to prevent layout shift */
        line-height: 1;
    }
    
    .bird-emoji {
        font-size: 5rem;
        transition: all 0.3s ease;
        display: inline-block;
        position: absolute;
        bottom: 0;
        left: 0;
    }
    
    .bird-emoji:hover {
        font-size: 8rem;
        transform: scale(1.2);
        color: black;
        filter: drop-shadow(0 0 15px rgba(0, 0, 0, 0.8));
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.7);
    }
    
    /* Dark shadow effect */
    .bird-emoji:hover::after {
        content: "";
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        height: 20px;
        background: radial-gradient(ellipse at center, rgba(0, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0) 80%);
        border-radius: 50%;
        z-index: -1;
    }
    </style>
    """

def get_bird_html():
    return """
    <div class="bird-container">
        <span class="bird-emoji">🐦</span>
    </div>
    """