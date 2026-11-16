"""Deterministic demo content: original editorial scripts, no external footage."""
from dataclasses import dataclass

@dataclass
class DemoScript:
    topic_title: str
    title: str
    hook: str
    narration: str
    duration_seconds: int
    visual_beats: list[str]
    youtube_description: str
    instagram_caption: str
    facebook_caption: str
    hashtags: list[str]

@dataclass
class DemoReport:
    approved_for_draft: bool
    claims: list[dict]
    rights_flags: list[str]
    corrections: list[str]
    overall_note: str

SCRIPTS = [
    DemoScript(
        "Why open-world games feel alive", "WHY OPEN WORLDS FEEL ALIVE", "A huge map is not what makes an open-world game feel alive.",
        "A huge map alone doesn't make an open-world game memorable. It's the little details. A city that changes with the time of day. Side characters who seem to have their own routines. Small discoveries that reward curiosity. The best open worlds make you forget the mission marker and just explore. What's the most alive game world you've played?",
        42, ["A giant map is only the beginning", "Worlds need believable routines", "Small details reward curiosity", "Exploration beats checklist gaming", "What's your most alive game world?"],
        "Why do some open-world games feel alive while others feel empty? Our take on world design.", "A big map isn't enough. The details make the world. 🎮", "What open-world game feels most alive to you?",
        ["Gaming", "OpenWorld", "GameDesign", "GameOn60"]),
    DemoScript(
        "Three questions before pre-ordering a game", "THINK BEFORE YOU PRE-ORDER", "Before you pre-order your next game, ask yourself these three questions.",
        "First: have you seen real gameplay, not just a cinematic trailer? Second: do you understand the performance and platform details for the device you own? Third: are you comfortable waiting for independent reviews? Hype is fun, but an informed purchase is better. What's your rule before pre-ordering a game?",
        40, ["Question one: Have you seen real gameplay?", "Question two: Does it suit your platform?", "Question three: Will you wait for reviews?", "Hype is fun; informed choices are better", "What's your pre-order rule?"],
        "A simple checklist for making smarter gaming purchases. Opinions, not financial advice.", "Pre-order hype vs informed decisions. What's your rule?", "Do you pre-order games or wait for reviews?",
        ["GamingTips", "GameBuying", "GamingCommunity", "GameOn60"]),
    DemoScript(
        "Why Football Manager saves become personal", "WHY FM SAVES GET PERSONAL", "How does a spreadsheet-heavy football game become an emotional roller coaster?",
        "Because a Football Manager save slowly becomes your story. The academy kid you trusted. The free transfer who became a club legend. The rival who keeps ruining your season. You start with a tactic and end up remembering entire careers. That's the magic of a long save. Which player became a legend in your save?",
        39, ["One academy prospect gets a chance", "A bargain signing becomes a hero", "A rival turns into a nemesis", "Your save becomes its own story", "Who is your club legend?"],
        "Why long Football Manager saves create stories that stay with you.", "Every long FM save has that one unexpected legend. ⚽", "Tell us about your biggest FM cult hero.",
        ["FootballManager", "FM", "SportsGaming", "GameOn60"]),
    DemoScript(
        "What makes a great sports game career mode", "THE CAREER MODE TEST", "A great career mode is about more than winning trophies.",
        "A great career mode gives you reasons to care between matches. Meaningful player development. Transfers that change your plans. Decisions with consequences. A season that tells a story beyond the final score. Graphics matter, but progression and immersion are what bring us back. What's the one feature every career mode needs?",
        40, ["Progression that feels earned", "Transfers with real consequences", "Choices that shape your journey", "Stories beyond the final score", "What feature is essential?"],
        "Our checklist for what makes a sports-game career mode worth playing.", "Career modes need stories, not just scorelines. 🏆", "What's your must-have career mode feature?",
        ["CareerMode", "SportsGames", "GamingOpinion", "GameOn60"]),
    DemoScript(
        "The perfect 60-second gaming review", "A GAME IN 60 SECONDS", "Can you decide whether a game is worth your time in just one minute?",
        "Try this quick review format. Start with the one thing the game does brilliantly. Then explain its biggest weakness. Say who will enjoy it most. Finish with one question: would you recommend it at its current price? A useful review doesn't need a score out of ten. It needs a clear point of view. What matters most to you in a review?",
        41, ["One thing it does brilliantly", "Its biggest weakness", "Who will enjoy it?", "Is it worth the asking price?", "What matters most in a review?"],
        "A repeatable framework for short, useful gaming reviews.", "One minute. One clear opinion. No filler. 🎮", "What do you look for in a gaming review?",
        ["GamingReviews", "GameReview", "GamingShorts", "GameOn60"]),
]

def get_demo_batch(count: int = 5):
    return SCRIPTS[:count]

def demo_report(script):
    return DemoReport(True, [{"claim": "Editorial opinion and general game-design commentary", "status": "OPINION", "evidence_url": None, "note": "Presented as original commentary, not a factual news claim."}], [], [], "Demo-mode original commentary. Verify all current or time-sensitive claims before using this format for news.")
