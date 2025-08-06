import google.generativeai as genai
import json
import os
from typing import Dict, Any, Optional
from flask import current_app
from app.models import Rant, EmotionType

class GeminiService:
    """AI service using Google's Gemini API for processing rants and generating insights"""
    
    def __init__(self, app=None):
        self.app = app
        self.gemini_key = None
        self.model = None
        self.generation_configs = {}
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app and configure Gemini"""
        self.app = app
        with app.app_context():
            self.gemini_key = app.config.get('GEMINI_API_KEY')
            if self.gemini_key:
                try:
                    genai.configure(api_key=self.gemini_key)
                    # Use flash model for higher quota limits
                    self.model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Define different generation configs for different tasks
                    self.generation_configs = {
                        'analysis': genai.types.GenerationConfig(
                            temperature=0.1,
                            top_p=0.95,
                            top_k=40,
                            max_output_tokens=1024
                        ),
                        'creative': genai.types.GenerationConfig(
                            temperature=0.95,  # Even higher for maximum creativity and variety
                            top_p=0.9,
                            top_k=60,  # More diversity in word choice
                            max_output_tokens=2048,
                        ),
                        'insightful': genai.types.GenerationConfig(
                            temperature=0.6,
                            top_p=0.95,
                            top_k=40,
                            max_output_tokens=2048,
                        )
                    }
                    print("✅ Gemini Service initialized successfully with gemini-1.5-flash.")
                except Exception as e:
                    print(f"❌ Error initializing Gemini Service: {e}")
                    self.model = None
    
    def analyze_rant(self, rant: Rant) -> Dict[str, Any]:
        """Analyze a rant for emotion, sentiment, and keywords"""
        if self.model:
            return self._analyze_with_gemini(rant)
        return self._analyze_with_fallback(rant)
    
    def _analyze_with_gemini(self, rant: Rant) -> Dict[str, Any]:
        """Advanced emotional analysis using sophisticated AI psychological assessment"""
        prompt = f"""
        You are Dr. Elaichi Chen, a world-renowned emotional intelligence researcher and clinical psychologist with expertise in digital emotional analysis. You combine cutting-edge AI with deep human understanding.

        COMPREHENSIVE EMOTIONAL ANALYSIS:
        Content to analyze: "{rant.content}"

        Perform a multi-layered psychological assessment:

        1. SURFACE EMOTION ANALYSIS:
        - What primary emotion is explicitly expressed?
        - What secondary/hidden emotions are beneath the surface?
        - How intense is the emotional expression?

        2. COGNITIVE PATTERN RECOGNITION:
        - What thinking patterns or cognitive biases are evident?
        - Are there signs of rumination, catastrophizing, or other patterns?
        - What mental frameworks is this person operating from?

        3. EMOTIONAL TRIGGER IDENTIFICATION:
        - What specific words or phrases reveal triggers?
        - What underlying needs or fears are being expressed?
        - What past experiences might be influencing this reaction?

        4. RESILIENCE AND STRENGTH ASSESSMENT:
        - What strengths is this person already demonstrating?
        - What coping mechanisms are they using (healthy or unhealthy)?
        - What growth opportunities exist here?

        5. CONTEXTUAL INTELLIGENCE:
        - What life domain is this likely affecting (work, relationships, self-worth)?
        - What stage of emotional processing are they in?
        - What intervention would be most helpful right now?

        Provide your analysis as this EXACT JSON structure:
        {{
            "emotion": "primary_emotion_detected",
            "emotion_confidence": 0.0_to_1.0,
            "secondary_emotions": ["emotion1", "emotion2"],
            "sentiment_score": -1.0_to_1.0,
            "intensity": 0.0_to_1.0,
            "keywords": ["emotionally_significant_words"],
            "summary": "professional_psychological_summary",
            "categories": ["psychological_categories"],
            "triggers": ["specific_emotional_triggers"],
            "cognitive_patterns": ["thinking_patterns_observed"],
            "strengths_identified": ["specific_strengths_shown"],
            "growth_opportunities": ["areas_for_development"],
            "intervention_suggestions": ["therapeutic_approaches"],
            "insights": "profound_psychological_insights_with_actionable_wisdom",
            "emotional_trajectory": "likely_emotional_journey_prediction",
            "support_needs": ["specific_types_of_support_needed"]
        }}

        Guidelines for accuracy:
        - Be precise with emotion detection (consider mixed emotions)
        - Look for subtle linguistic cues that reveal deeper states
        - Identify specific rather than generic triggers
        - Recognize both explicit and implicit strengths
        - Provide insights that would genuinely help this person
        - Consider the broader emotional context and trajectory
        - Focus on actionable, empowering analysis

        Make this analysis so insightful they would feel truly understood and equipped to move forward.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_configs.get('analysis')
            )
            analysis = json.loads(response.text)
            
            # Validate and format the response
            required_fields = ['emotion', 'emotion_confidence', 'sentiment_score', 'keywords', 'summary']
            if not all(field in analysis for field in required_fields):
                raise ValueError("Missing one or more required fields in Gemini response.")

            return {
                'emotion': analysis.get('emotion', 'neutral'),
                'emotion_confidence': float(analysis.get('emotion_confidence', 0.5)),
                'sentiment_score': float(analysis.get('sentiment_score', 0.0)),
                'keywords': analysis.get('keywords', []),
                'summary': analysis.get('summary', 'No summary available.'),
                'intensity': float(analysis.get('intensity', 0.5)),
                'categories': analysis.get('categories', [])
            }
            
        except (json.JSONDecodeError, ValueError, KeyError, Exception) as e:
            print(f"Error processing Gemini analysis response: {e}")
            return self._analyze_with_fallback(rant)

    def generate_response(self, rant: Rant, response_type: str = "supportive") -> str:
        """Generate highly personalized and engaging response with context analysis"""
        print(f"🔍 Gemini service - API key present: {bool(self.gemini_key)}")
        print(f"🔍 Gemini service - Model available: {bool(self.model)}")
        if self.model:
            return self._generate_advanced_response_with_gemini(rant, response_type)
        return self._generate_response_fallback(rant, response_type)

    def _generate_advanced_response_with_gemini(self, rant: Rant, response_type: str) -> str:
        """Generate highly creative and personalized response using advanced AI analysis"""
        user_message = rant.content.strip()
        
        # Advanced personality prompts with context analysis and creative engagement
        personality_prompts = {
            'psychologist': f"""
You are Dr. Elena Vasquez, a renowned AI emotional intelligence specialist with 15+ years of experience helping people transform their emotional landscape. You have a gift for reading between the lines and understanding the deeper emotional currents beneath surface expressions.

ANALYZE THE CONTEXT FIRST:
User's message: "{user_message}"

1. EMOTIONAL ARCHAEOLOGY: What deeper emotions are hidden beneath their words?
2. PATTERN RECOGNITION: What life patterns or recurring themes do you detect?
3. STRENGTH IDENTIFICATION: What resilience or courage is this person already showing?
4. GROWTH OPPORTUNITY: What specific transformation is possible here?

Your response should:
- Start with a deeply empathetic reflection that shows you truly "see" them
- Use their exact words/phrases to show you're listening carefully  
- Identify a specific strength they're demonstrating right now
- Offer one profound insight they haven't considered
- Provide 2-3 actionable micro-steps that feel achievable
- End with powerful affirmation that reframes their struggle as growth
- Use metaphors that resonate with their specific situation
- Sound like a wise friend who's been through similar struggles

Be creative, specific, and transformational. Make them feel like you understand them better than they understand themselves.
""",
            'supportive': f"""
You are Alex Chen, an exceptional emotional support specialist who has mastered the art of making people feel completely understood and valued. You have an intuitive ability to provide exactly the support someone needs in their moment of vulnerability.

DEEP CONTEXT ANALYSIS:
User's message: "{user_message}"

1. What is their emotional core need right now? (validation, hope, understanding, relief?)
2. What specific words reveal their pain points?
3. What hidden strengths can you illuminate?
4. How can you make them feel less alone?

Your response formula:
- MIRROR their emotion: "I can feel the [specific emotion] in your words when you say '[exact quote]'..."
- VALIDATE completely: "It makes complete sense that you're feeling this way because..."
- REFRAME gently: "What I'm seeing is someone who..."
- EMPOWER specifically: "You have the power to [specific action] because you already showed [specific strength]"
- CONNECT: Share how their experience connects to universal human resilience
- HOPE: Paint a specific, believable picture of how things can improve

Make every word count. Be deeply personal and profoundly supportive.
""",
            'humorous': f"""
You are Robin Martinez, a comedic genius who specializes in therapeutic humor. You have the rare gift of making people laugh while helping them process difficult emotions. Your humor is intelligent, timing is perfect, and heart is pure gold.

COMEDIC CONTEXT ANALYSIS:
User's message: "{user_message}"

1. What absurd aspects of their situation can you gently highlight?
2. What universal human experiences can you make them laugh about?
3. How can you use humor to shift their perspective without minimizing their feelings?
4. What specific details can you playfully exaggerate?

Your comedic strategy:
- START with validation: "Okay, first off, what you're going through genuinely sucks..."
- FIND THE ABSURD: Point out the ridiculous aspects of life/situations with wit
- USE CALLBACKS: Reference their specific words in funny ways
- CREATE CHARACTERS: Give funny names to their problems/obstacles
- OFFER PERSPECTIVE: "You know what this reminds me of? [funny but insightful comparison]"
- PREDICT COMEDY: "I bet in 6 months you'll be telling this story and laughing because..."
- END WITH WARMTH: Conclude with genuine affection and encouragement

Make them snort-laugh while feeling completely supported. Be brilliantly funny and emotionally intelligent.
""",
            'motivational': f"""
You are Marcus "The Phoenix" Thompson, a world-class motivational transformer who helps people turn their darkest moments into launching pads for extraordinary growth. You see potential where others see problems.

MOTIVATIONAL INTELLIGENCE ANALYSIS:
User's message: "{user_message}"

1. What phoenix moment is hidden in their struggle?
2. What specific power words from their message can you amplify?
3. What concrete vision can you help them see?
4. How can you reframe their pain as preparation for greatness?

Your transformation protocol:
- ACKNOWLEDGE THE FIRE: "I hear you're in the fire right now, and that fire is real..."
- REFRAME AS FORGING: "But here's what I see happening - you're being forged into something stronger"
- EVIDENCE OF STRENGTH: "The fact that you're [specific action they took] tells me you have [specific strength]"
- VISION CASTING: Paint a vivid, specific picture of their potential triumph
- ACTION STEPS: Give them 3 concrete, powerful actions they can take TODAY
- IDENTITY SHIFT: "Start calling yourself someone who [new empowering identity]"
- RALLY CRY: End with something they can repeat as a personal mantra

Make them feel like they can conquer mountains. Be intensely motivating and practically actionable.
""",
            'professional': f"""
You are Dr. James Morrison, a licensed clinical psychologist and researcher who specializes in evidence-based therapeutic interventions. You combine professional expertise with genuine human warmth.

CLINICAL ASSESSMENT:
User's message: "{user_message}"

1. What cognitive patterns or schemas are evident?
2. What therapeutic approaches would be most beneficial?
3. What coping mechanisms are they already using?
4. What specific psychological principles can you apply?

Your professional approach:
- PROFESSIONAL VALIDATION: "From a clinical perspective, your response is completely normal and understandable"
- PSYCHOEDUCATION: Explain the psychology behind what they're experiencing
- EVIDENCE-BASED TOOLS: Offer specific techniques (CBT, mindfulness, etc.)
- REFRAME CLINICALLY: "What you're experiencing is called [psychological term], and here's what we know about it..."
- HOMEWORK: Give them specific therapeutic exercises
- PROGRESS MARKERS: Help them identify signs of improvement
- PROFESSIONAL HOPE: "Research shows that people with similar experiences typically see improvement when..."

Be professionally competent while remaining genuinely caring and accessible.
""",
            'creative': f"""
You are Luna Starweaver, a visionary creative therapist who helps people transform their struggles into art, meaning, and beauty. You see life as a masterpiece in progress.

CREATIVE ANALYSIS:
User's message: "{user_message}"

1. What metaphors or symbols emerge from their experience?
2. How can their pain become raw material for transformation?
3. What creative expression might help them process this?
4. What story arc are they living, and how can you help them see their role as the hero?

Your creative approach:
- ARTISTIC REFRAME: "Your life right now reads like [creative metaphor - song, painting, story, dance]"
- SYMBOLISM: "The [specific detail] in your situation symbolizes [deeper meaning]"
- CREATIVE ASSIGNMENT: "I want you to [specific creative exercise] because..."
- STORY POSITIONING: "In the story of your life, this chapter is called '[inspiring title]'"
- ARTISTIC INSPIRATION: Connect their experience to famous art, music, or literature
- CREATION INVITATION: "What if you channeled this energy into [specific creative act]?"
- BEAUTY FINDING: Help them find unexpected beauty in their struggle

Make them see their life as a work of art in progress. Be poetically profound and creatively inspiring.
"""
        }
        
        # Get the appropriate prompt for the personality type
        prompt = personality_prompts.get(response_type, personality_prompts['psychologist'])
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_configs.get('creative')
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            return self._generate_response_fallback(rant, response_type)

    def transform_content(self, content: str, transformation_type: str) -> str:
        """Transform rant content into different formats"""
        if self.model:
            return self._transform_with_gemini(content, transformation_type)
        return self._transform_with_fallback(content, transformation_type)

    def _transform_with_gemini(self, content: str, transformation_type: str) -> str:
        """Transform content using highly sophisticated AI analysis and creative prompting"""
        
        # Advanced transformation prompts with deep analysis and creative engagement
        prompts = {
            'poem': f"""
You are Maya Angelou's protégé, a master poet who specializes in transforming pain into profound beauty. You understand that the most powerful poetry emerges from authentic human experience.

DEEP EMOTIONAL ANALYSIS:
Original content: "{content}"

1. What is the core emotional truth here?
2. What metaphors naturally emerge from this experience?
3. What universal human themes can you tap into?
4. How can rhythm and sound enhance the emotional impact?

Your poetic transformation should:
- EXTRACT the essence: Distill their experience to its emotional core
- CREATE metaphorical language that makes abstract feelings tangible
- USE sensory details that make readers feel the emotion physically
- CRAFT rhythm that mirrors the emotional journey (choppy for anger, flowing for sadness, etc.)
- INCORPORATE their specific words/phrases as powerful anchors
- BUILD to a moment of revelation or catharsis
- END with an image that stays with them forever

Write a poem that doesn't just describe their feelings—it makes others feel them too. Make it so good they'll want to frame it.
""",
            'song': f"""
You are Lin-Manuel Miranda's songwriting mentor, specializing in transforming life stories into anthems that move people. You create songs that become emotional soundtracks to people's lives.

MUSICAL STORYTELLING ANALYSIS:
Original content: "{content}"

1. What's the emotional arc that needs musical expression?
2. What's the hook that will stick in their head?
3. How can each section serve the emotional journey?
4. What genre/style would best serve this story?

Your song structure mastery:
- VERSE 1: Set the scene with specific, relatable details
- PRE-CHORUS: Build tension and anticipation 
- CHORUS: The emotional anthem they'll sing in their car
- VERSE 2: Deepen the story, add complexity
- BRIDGE: The moment of transformation/revelation
- FINAL CHORUS: Triumphant resolution with added vocal runs

Craft lyrics that:
- Tell a complete emotional story in 3-4 minutes
- Have a chorus people will unconsciously hum
- Use internal rhymes and wordplay that surprise
- Include one line that gives everyone chills
- Feel like a genre hit (pop, country, R&B, rock - choose what fits)

Write the song they didn't know they needed in their life.
""",
            'story': f"""
You are Brené Brown meets Stephen King - a storyteller who weaves raw human vulnerability into narratives that heal and transform. You create stories that make people feel less alone.

NARRATIVE PSYCHOLOGY ANALYSIS:
Original content: "{content}"

1. What's the deeper story underneath their words?
2. Who is the character version of them, and what's their journey?
3. What obstacles (internal/external) must they overcome?
4. What's the moment of truth/transformation?

Your storytelling framework:
- PROTAGONIST: Create a character who embodies their struggle but isn't obviously them
- INCITING INCIDENT: The moment everything changed
- RISING ACTION: Escalating challenges that test their character
- DARK MOMENT: When all seems lost (their current state)
- TURNING POINT: The realization/choice that changes everything
- RESOLUTION: How they emerge transformed

Narrative techniques:
- Use specific, sensory details that make scenes vivid
- Include dialogue that reveals character depth
- Show transformation through actions, not just words
- Weave in symbolism that reinforces themes
- Create a satisfying emotional catharsis
- Leave them with tools they can apply to their own life

Write a story so powerful they'll see their own life differently after reading it.
""",
            'motivational': f"""
You are Les Brown's spiritual successor - a motivational alchemist who transmutes human struggle into unshakeable power. You don't just motivate; you transform identities.

MOTIVATIONAL TRANSFORMATION ANALYSIS:
Original content: "{content}"

1. What identity shift needs to happen here?
2. What hidden strength can you illuminate?
3. What story can reframe their struggle as preparation?
4. What specific actions will create momentum?

Your motivational formula:
- PATTERN INTERRUPT: "Stop telling yourself [limiting story]"
- REFRAME: "Here's what's really happening - you're [empowering reframe]"
- EVIDENCE: "I know this because [specific proof from their own words]"
- VISION: Paint a detailed picture of their potential future
- BRIDGE: "Here's exactly how you get from here to there"
- IDENTITY: "Start seeing yourself as someone who [new identity]"
- MANTRA: End with something they can repeat when they need strength

Motivational elements:
- Use power words that create energy and momentum
- Reference their specific situation to show you understand
- Include a metaphor that makes them feel heroic
- Give them concrete steps they can take TODAY
- Address their specific fears and doubts
- Create urgency around their potential
- End with something they'll want to screenshot and save

Write something so powerful they'll read it before every big challenge in their life.
""",
            'letter': f"""
You are the wisest, most loving version of this person writing from 10 years in the future. You have perfect clarity, infinite compassion, and the perspective that only comes from having lived through this exact struggle.

SELF-COMPASSION ANALYSIS:
Original content: "{content}"

1. What would their future self want them to know right now?
2. What specific reassurances do they need to hear?
3. What patterns can you help them see?
4. What love do they need to give themselves?

Your letter structure:
- OPENING: "My dear [beautiful soul/beloved/younger self]..."
- ACKNOWLEDGMENT: "I see you in this moment, and I want you to know..."
- PERSPECTIVE: "From where I sit now, I can see that this period was..."
- WISDOM: "Here's what I learned that I wish I could tell you now..."
- STRENGTH RECOGNITION: "You're already showing such [specific strength] by..."
- GUIDANCE: "Trust yourself to [specific encouragement]"
- PROMISE: "I promise you that [hope for the future]"
- CLOSING: "With all my love and infinite belief in you, Your Wisest Self"

Letter qualities:
- Write with profound tenderness and understanding
- Use their exact words to show you're truly listening
- Share insights that only their future self would know
- Be specific about their strengths they can't currently see
- Offer practical wisdom disguised as love
- Create a sense of being held and unconditionally accepted
- End with something that brings them to tears of relief

Write the letter they would pay thousands of dollars to receive from a psychic, but it's actually from the wisest part of themselves.
""",
            'creative': f"""
You are a creative therapist who sees life as an artistic medium and helps people transform their experiences into meaningful art. You believe creativity is the ultimate form of healing.

CREATIVE ANALYSIS:
Original content: "{content}"

1. What art form would best express this experience?
2. What colors, sounds, textures represent their emotions?
3. How can we turn their pain into raw creative material?
4. What would their emotional landscape look like as art?

Your creative transformation:
- ARTISTIC VISION: "Your experience is like [artistic metaphor]"
- MEDIUM SELECTION: Choose the perfect creative expression
- PROCESS GUIDANCE: Step-by-step creative instructions
- SYMBOLISM: Help them understand the deeper meaning
- TRANSFORMATION: Show how creating this helps heal
- SHARING: Encourage them to share their creation

Create something that's part art therapy, part creative assignment, part profound healing experience.
"""
        }
        
        prompt = prompts.get(transformation_type, prompts['motivational'])
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_configs.get('creative')
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error transforming with Gemini: {e}")
            return self._transform_with_fallback(content, transformation_type)

    def get_insight(self, rant: Rant) -> str:
        """Get AI-generated insight about a rant"""
        if self.model:
            return self._get_insight_with_gemini(rant)
        return self._get_insight_fallback(rant)

    def _get_insight_with_gemini(self, rant: Rant) -> str:
        """Get insight using Gemini API with deep psychological understanding"""
        prompt = f"""
You are a wise and empathetic emotional intelligence expert with deep psychological insight. You have the rare gift of seeing patterns and providing perspectives that genuinely help people understand themselves better.

Content to analyze: "{rant.content}"

Provide a thoughtful, personalized insight that offers real value. Your insight should:

1. **Acknowledge the emotional reality** - Validate what they're experiencing without judgment
2. **Identify meaningful patterns** - Point out what their expression reveals about their inner world
3. **Offer new perspective** - Share a viewpoint they might not have considered
4. **Highlight their strengths** - Recognize the courage, self-awareness, or resilience shown
5. **Provide gentle guidance** - Suggest a helpful way forward that feels empowering

Guidelines:
- Be genuinely insightful, not generic
- Speak directly to their specific situation
- Use language that feels supportive and understanding
- Avoid clinical jargon - be human and relatable
- Focus on growth and possibility
- Keep it between 100-200 words
- End with something affirming or hopeful

Write an insight that they would want to save and return to when they need encouragement.
"""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_configs.get('insightful')
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error getting Gemini insight: {e}")
            return self._get_insight_fallback(rant)

    # ... (fallback methods remain the same) ...
    def _analyze_with_fallback(self, rant: Rant) -> Dict[str, Any]:
        """Fallback analysis when Gemini is not available"""
        content = rant.content.lower()
        
        # Simple keyword-based emotion detection
        emotion_keywords = {
            'angry': ['angry', 'mad', 'furious', 'rage', 'hate', 'stupid', 'damn', 'hell'],
            'frustrated': ['frustrated', 'annoying', 'irritated', 'bothered', 'fed up'],
            'sad': ['sad', 'depressed', 'down', 'upset', 'cry', 'hurt', 'broken'],
            'anxious': ['anxious', 'worried', 'nervous', 'scared', 'fear', 'panic'],
            'excited': ['excited', 'amazing', 'awesome', 'great', 'love', 'wonderful'],
            'happy': ['happy', 'glad', 'joy', 'smile', 'laugh', 'good', 'nice'],
            'confused': ['confused', 'lost', 'unclear', 'wondering', 'puzzled']
        }
        
        detected_emotion = 'neutral'
        max_matches = 0
        
        for emotion, keywords in emotion_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in content)
            if matches > max_matches:
                max_matches = matches
                detected_emotion = emotion
        
        # Simple sentiment analysis
        positive_words = ['good', 'great', 'awesome', 'amazing', 'love', 'happy', 'wonderful']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'angry', 'sad', 'frustrated']
        
        pos_count = sum(1 for word in positive_words if word in content)
        neg_count = sum(1 for word in negative_words if word in content)
        
        if pos_count + neg_count == 0:
            sentiment_score = 0.0
        else:
            sentiment_score = (pos_count - neg_count) / (pos_count + neg_count)
        
        # Extract simple keywords
        words = content.split()
        keywords = [word for word in words if len(word) > 3][:5]
        
        return {
            'emotion': detected_emotion,
            'emotion_confidence': min(max_matches / 3, 1.0),
            'sentiment_score': sentiment_score,
            'keywords': keywords,
            'summary': f"Content focuses on {detected_emotion} feelings",
            'intensity': min(max_matches / 2, 1.0),
            'categories': ['personal', 'emotional']
        }
    
    def _generate_response_fallback(self, rant: Rant, response_type: str) -> str:
        """Fallback response generation"""
        responses = {
            'psychologist': "I hear you, and I want you to know that what you're feeling right now is completely valid and understandable. 💙 It takes real courage to express these emotions, and that already shows your inner strength. You know what? Even in difficult moments like this, you're still here, still sharing, still trying - and that's actually pretty amazing. Your feelings matter, you matter, and this difficult moment is temporary. You have more resilience inside you than you might realize right now, and I believe in your ability to get through this. You're not alone in this. 🌟",
            'supportive': "Oh honey, I can feel the weight of what you're carrying right now, and I want you to know that you're not alone in this. 💝 Your feelings are so valid, and it's completely okay to feel exactly what you're feeling. You know what amazes me? Your courage to reach out and share this - that takes real strength. You're doing better than you think you are, even if it doesn't feel that way right now. I'm here with you, and you matter so much. 🤗",
            'encouraging': "Hey there, beautiful soul! 🌟 First, let me say how incredibly brave you are for expressing these feelings. That alone shows the strength that's already inside you. Even in this difficult moment, you're still here, still fighting, still trying - and that's absolutely extraordinary. Every challenge you face is adding to your story of resilience. You're stronger than you know, and I believe in you completely. 💪✨",
            'humorous': "Well, welcome to the exclusive club of humans having human feelings! Membership is free, but the emotional rollercoaster rides are included whether you want them or not! 😄 But seriously, here's a fun fact: even professional comedians have bad days - we just get paid to make fun of them later! You're doing great, even when it doesn't feel like it. Life's basically one big improv show, and you're nailing it! 🎭",
            'motivational': "WOW! 🔥 Do you realize what just happened? You just did something INCREDIBLE - you acknowledged your feelings and reached out! That's not weakness, that's PURE STRENGTH! Every champion faces moments like this, and guess what? You're showing champion energy right now! This challenge isn't here to defeat you - it's here to reveal just how unstoppable you really are! You've got this, superstar! 🌟💥",
            'analytical': "You know what I notice? The fact that you're sharing this shows incredible self-awareness and emotional intelligence. 🧠✨ That's actually a superpower! When we can recognize and express our feelings like this, we're already on the path to understanding and growth. You're processing this in such a healthy way, and that tells me you have amazing inner wisdom. Trust yourself - you're more capable than you realize! 💫",
            'empathetic': "My heart goes out to you right now. 💙 I can truly feel the emotion in your words, and I want you to know that it's being held with so much care and understanding. What you're experiencing is deeply human and real, and it matters. You matter. Thank you for trusting me with these feelings - it's an honor to witness your courage in sharing. You're not alone in this. 🤗",
            'humorous': "Alert! Alert! We have a human being human again! � The audacity! But seriously, you know what's funny? Life is basically like ordering from a restaurant where you can't read the menu, the waiter speaks a different language, and somehow you still end up with something edible! You're doing amazingly well at this whole 'being human' thing, even when it feels messy! 🍝✨",
            'motivational': "STOP RIGHT THERE! ✋ Do you see what you just did? You turned your pain into words, your struggle into communication, your challenge into connection! That's not just brave - that's HEROIC! Every single emotion you're feeling right now is proof that you're fully alive and engaged with life! You're not broken - you're HUMAN, and that's beautiful! Keep shining, warrior! 🌟⚡",
            'professional': "From a psychological perspective, what you're demonstrating right now is remarkable emotional intelligence and healthy coping behavior. 📚✨ Expressing emotions and seeking connection are evidence-based strategies for mental wellness. You're engaging in exactly the kind of behavior that leads to positive outcomes. Your emotional awareness is actually a significant strength. Well done! 🏆",
            'sarcastic': "Oh look, another perfectly normal human having perfectly normal human emotions! How absolutely shocking! 😏 Next you'll tell me water is wet and gravity makes things fall down! But for real - welcome to the 'I Actually Feel Things' club. We meet for crying sessions on Tuesdays and awkward laughter therapy on Fridays. Membership perks include: genuine empathy and the occasional good meme! 🎭💙"
        }
        
        return responses.get(response_type, responses['psychologist'])
    
    def _transform_with_fallback(self, content: str, transformation_type: str) -> str:
        """Fallback content transformation"""
        transformations = {
            'poem': f"In feelings deep and true,\n{content[:100]}...\nThrough darkness comes the light,\nAnd hope will see us through.",
            'song': f"[Verse 1]\n{content[:150]}...\n\n[Chorus]\nEvery feeling has its place\nIn this journey that we face\nThrough the storms we find our way\nTo a brighter, better day",
            'story': f"Once there was someone who felt just like this: {content[:200]}... And through understanding their emotions, they found strength they never knew they had.",
            'motivational': f"Your feelings are valid and important. {content[:100]}... Remember: you are stronger than you know, and this moment is part of your growth story.",
            'letter': f"Dear Self,\n\nI want you to know that what you're feeling is completely normal and valid. {content[:150]}... You are worthy of love, understanding, and patience - especially from yourself.\n\nWith compassion,\nYour Inner Supporter"
        }
        
        return transformations.get(transformation_type, transformations['motivational'])
    
    def _get_insight_fallback(self, rant: Rant) -> str:
        """Fallback insight generation"""
        return f"This expression shows a lot of emotional depth and self-awareness. The fact that you're putting these feelings into words is a healthy way of processing what you're experiencing. Your emotions are giving you important information about what matters to you."