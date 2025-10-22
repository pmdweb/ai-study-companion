"""
STAR Methodology Evaluation Module
Evaluates interview responses using STAR framework and provides rewriting functionality
"""

import re
from typing import Dict, List, Optional

def score_star(response: str) -> Dict:
    """
    Evaluate response text using STAR methodology
    
    Args:
        response (str): User's interview response
        
    Returns:
        dict: STAR scores and feedback
    """
    response = response.lower().strip()
    
    # Initialize scores
    scores = {
        'situation': {'score': 0, 'feedback': ''},
        'task': {'score': 0, 'feedback': ''},
        'action': {'score': 0, 'feedback': ''},
        'result': {'score': 0, 'feedback': ''},
        'total_score': 0,
        'suggestions': []
    }
    
    # Situation scoring (context, setting, problem)
    situation_keywords = ['when', 'where', 'company', 'project', 'team', 'client', 'problem', 'challenge']
    situation_score = 0
    
    if any(keyword in response for keyword in situation_keywords):
        situation_score += 1
        
    if len([word for word in situation_keywords if word in response]) >= 3:
        situation_score += 1
        
    scores['situation']['score'] = situation_score
    scores['situation']['feedback'] = _get_situation_feedback(situation_score)
    
    # Task scoring (objective, responsibility, goal)
    task_keywords = ['responsible', 'goal', 'objective', 'task', 'needed to', 'had to', 'my role']
    task_score = 0
    
    if any(keyword in response for keyword in task_keywords):
        task_score += 1
        
    if 'my' in response and any(word in response for word in ['responsibility', 'goal', 'task']):
        task_score += 1
        
    scores['task']['score'] = task_score
    scores['task']['feedback'] = _get_task_feedback(task_score)
    
    # Action scoring (specific steps, verbs)
    action_verbs = ['implemented', 'created', 'developed', 'analyzed', 'organized', 'coordinated', 'led', 'designed']
    action_score = 0
    
    action_count = len([verb for verb in action_verbs if verb in response])
    if action_count >= 1:
        action_score += 1
    if action_count >= 3:
        action_score += 1
        
    scores['action']['score'] = action_score
    scores['action']['feedback'] = _get_action_feedback(action_score)
    
    # Result scoring (outcomes, metrics, impact)
    result_patterns = [r'\d+%', r'\d+\s*(hours?|days?|weeks?|months?)', r'\$\d+', r'\d+\s*(people|users|customers)']
    numbers_found = any(re.search(pattern, response) for pattern in result_patterns)
    
    result_keywords = ['improved', 'increased', 'decreased', 'saved', 'reduced', 'achieved', 'delivered']
    result_score = 0
    
    if any(keyword in response for keyword in result_keywords):
        result_score += 1
        
    if numbers_found:
        result_score += 1
    else:
        scores['suggestions'].append("Include specific metrics and numbers in your results")
        
    scores['result']['score'] = result_score
    scores['result']['feedback'] = _get_result_feedback(result_score)
    
    # Calculate total and overall suggestions
    scores['total_score'] = sum(scores[key]['score'] for key in ['situation', 'task', 'action', 'result'])
    
    if scores['total_score'] < 4:
        scores['suggestions'].append("Focus on providing more specific details in each STAR component")
        
    return scores

def _get_situation_feedback(score: int) -> str:
    """Get feedback for situation score"""
    if score == 0:
        return "Missing context. Add when/where this happened, what company/project, what problem you faced."
    elif score == 1:
        return "Basic context provided. Consider adding more specific details about the setting."
    else:
        return "Good situational context provided."

def _get_task_feedback(score: int) -> str:
    """Get feedback for task score"""
    if score == 0:
        return "Unclear what your specific responsibility was. State your role and what you needed to accomplish."
    elif score == 1:
        return "Task mentioned but could be clearer. Be more specific about your objective."
    else:
        return "Clear task and responsibility identified."

def _get_action_feedback(score: int) -> str:
    """Get feedback for action score"""
    if score == 0:
        return "Missing specific actions. Use action verbs and describe the steps you took."
    elif score == 1:
        return "Some actions mentioned. Add more specific details about what you did."
    else:
        return "Good variety of specific actions described."

def _get_result_feedback(score: int) -> str:
    """Get feedback for result score"""
    if score == 0:
        return "No clear results or outcomes mentioned. Add what you achieved and include numbers/metrics."
    elif score == 1:
        return "Results mentioned but missing metrics. Add specific numbers to quantify your impact."
    else:
        return "Good results with quantifiable impact."

def rewrite_response(question: str, response: str) -> Dict:
    """
    Rewrite a weak response into proper STAR format
    
    Args:
        question (str): The interview question asked
        response (str): User's original response
        
    Returns:
        dict: Contains rewritten response and follow-up questions
    """
    try:
        # Validate inputs
        if not question or not response:
            return {
                'rewritten_response': "Please provide both a question and response to generate improvements.",
                'follow_up_questions': [],
                'improvement_notes': "Invalid input provided."
            }
        
        # Get current evaluation to understand weaknesses
        evaluation = score_star(response)
        total_score = evaluation['total_score']
        
        # If response is already strong (6+ out of 8), minimal changes needed
        if total_score >= 6:
            return {
                'rewritten_response': _enhance_strong_response(response),
                'follow_up_questions': _generate_follow_ups(question, response),
                'improvement_notes': "Response was already strong. Minor enhancements made for clarity."
            }
        
        # For weak responses, perform comprehensive rewrite
        rewritten = _comprehensive_rewrite(question, response, evaluation)
        
        return {
            'rewritten_response': rewritten,
            'follow_up_questions': _generate_follow_ups(question, rewritten),
            'improvement_notes': "Response restructured using STAR methodology with specific examples and metrics."
        }
        
    except Exception as e:
        # Fallback response if something goes wrong
        return {
            'rewritten_response': f"Error generating rewrite: {str(e)}. Please try with a different response.",
            'follow_up_questions': [],
            'improvement_notes': f"Technical error occurred: {str(e)}"
        }

def _comprehensive_rewrite(question: str, original_response: str, evaluation: Dict) -> str:
    """
    Perform comprehensive STAR rewrite for weak responses
    """
    # Extract any useful content from original response
    original_lower = original_response.lower()
    
    # Template-based rewrite with enhanced content
    situation_template = _generate_situation_content(original_response, evaluation)
    task_template = _generate_task_content(original_response, evaluation)
    action_template = _generate_action_content(original_response, evaluation)
    result_template = _generate_result_content(original_response, evaluation)
    
    rewritten = f"""**Situation:** {situation_template}

**Task:** {task_template}

**Action:** {action_template}

**Result:** {result_template}"""
    
    return rewritten

def _generate_situation_content(original: str, evaluation: Dict) -> str:
    """Generate enhanced Situation content based on original response"""
    try:
        original_lower = original.lower()
        
        # Analyze the original response for context clues
        if 'bug' in original_lower or 'fix' in original_lower or 'error' in original_lower:
            return "At my previous company, we discovered a critical system bug that was affecting user productivity and causing data inconsistencies. This issue emerged during our peak usage hours when downtime would have the maximum business impact."
        
        elif 'team' in original_lower or 'colleague' in original_lower:
            return "In my role as team lead, we were facing interpersonal challenges that were impacting project delivery and team morale. The situation developed when conflicting work styles and communication preferences created tension within our cross-functional team."
        
        elif 'deadline' in original_lower or 'time' in original_lower:
            return "During Q4 at my previous organization, we received an urgent client request with an extremely tight deadline that required us to compress a typical 3-month project into 3 weeks. This coincided with several team members being on planned leave."
        
        elif 'project' in original_lower:
            return "While working on a high-visibility project at [Company], we encountered unexpected technical constraints that threatened to derail our delivery timeline. The project was critical for our department's annual objectives and had executive visibility."
        
        else:
            # Generic but improved version
            return "In my previous role at [Company Name], we faced a complex challenge that required both technical expertise and strategic thinking. The situation was time-sensitive and had potential implications for both our team's performance and broader organizational goals."
            
    except Exception:
        return "At my previous company, we encountered a significant challenge that required immediate attention and collaborative problem-solving."

def _generate_task_content(original: str, evaluation: Dict) -> str:
    """Generate enhanced Task content based on original response"""
    try:
        original_lower = original.lower()
        
        if 'bug' in original_lower or 'fix' in original_lower:
            return "I was tasked with identifying the root cause of the system bug, implementing a comprehensive fix, and ensuring no data loss occurred. My responsibility included coordinating with the QA team and communicating status updates to stakeholders."
            
        elif 'team' in original_lower:
            return "My objective was to resolve the team dynamics issues while maintaining project momentum and team morale. I needed to facilitate better communication, address underlying concerns, and establish sustainable working relationships."
            
        elif 'deadline' in original_lower or 'time' in original_lower:
            return "I was responsible for reorganizing the project timeline, reallocating resources, and finding creative solutions to meet the compressed deadline without sacrificing quality standards."
            
        elif 'project' in original_lower:
            return "My task was to assess the technical constraints, develop alternative approaches, and ensure the project stayed on track while managing stakeholder expectations throughout the process."
            
        else:
            return "I was specifically assigned to lead the resolution effort, coordinate with relevant stakeholders, and implement a solution that addressed both immediate needs and long-term sustainability."
            
    except Exception:
        return "I was responsible for taking ownership of the challenge and delivering a comprehensive solution within the required timeframe."

def _generate_action_content(original: str, evaluation: Dict) -> str:
    """Generate enhanced Action content based on original response"""
    try:
        original_lower = original.lower()
        
        if 'bug' in original_lower or 'fix' in original_lower:
            return """I took a systematic debugging approach:

1. **Analyzed** server logs and error reports to identify patterns and potential root causes
2. **Reproduced** the issue in a staging environment to understand the exact failure conditions  
3. **Collaborated** with senior developers to review code changes and validate my hypothesis
4. **Implemented** a targeted fix that addressed the core issue without affecting other system components
5. **Tested** the solution thoroughly in multiple environments before deploying to production
6. **Monitored** system performance post-deployment to ensure the fix was effective"""
            
        elif 'team' in original_lower:
            return """I addressed the team challenges through structured intervention:

1. **Conducted** individual meetings with each team member to understand their perspectives and concerns
2. **Facilitated** a team retrospective to identify communication gaps and workflow issues
3. **Established** clearer role definitions and communication protocols for the team
4. **Implemented** regular check-ins and collaborative tools to improve information sharing
5. **Provided** coaching and mediation to help team members work through interpersonal conflicts
6. **Monitored** team dynamics and adjusted approaches based on ongoing feedback"""
            
        elif 'deadline' in original_lower or 'time' in original_lower:
            return """I restructured our approach to meet the compressed timeline:

1. **Analyzed** project requirements to identify must-have vs. nice-to-have features
2. **Negotiated** scope adjustments with stakeholders to focus on core deliverables
3. **Reorganized** team assignments to maximize efficiency and leverage individual strengths
4. **Implemented** daily standups and progress tracking to maintain momentum
5. **Coordinated** with external vendors to expedite critical resource procurement  
6. **Established** contingency plans for potential roadblocks and resource constraints"""
            
        else:
            return """I approached the challenge with a structured methodology:

1. **Assessed** the current situation by gathering data and stakeholder input
2. **Analyzed** root causes and identified key constraints and opportunities
3. **Developed** multiple solution options with clear pros, cons, and resource requirements
4. **Collaborated** with cross-functional teams to validate approaches and gain buy-in
5. **Implemented** the chosen solution with careful change management and communication
6. **Monitored** progress and made adjustments based on real-time feedback and results"""
            
    except Exception:
        return "I took systematic action by analyzing the problem, developing a comprehensive plan, collaborating with relevant stakeholders, implementing targeted solutions, and monitoring results throughout the process."

def _generate_result_content(original: str, evaluation: Dict) -> str:
    """Generate enhanced Result content based on original response"""
    try:
        original_lower = original.lower()
        has_numbers = bool(re.search(r'\d+', original))
        
        if 'bug' in original_lower or 'fix' in original_lower:
            return """This systematic approach delivered strong results:

• **Resolution Time:** Fixed the critical bug within 6 hours, minimizing user impact
• **System Stability:** Achieved 99.9% uptime in the following month, up from 94% 
• **User Experience:** Reduced user-reported errors by 85% and improved response times by 40%
• **Process Improvement:** Implemented automated testing that catches similar issues before production
• **Cost Impact:** Prevented an estimated $75,000 in lost productivity and customer churn
• **Recognition:** Received "Problem Solver of the Quarter" award for rapid and effective resolution"""
            
        elif 'team' in original_lower:
            return """The team intervention produced significant improvements:

• **Team Dynamics:** Achieved 90% improvement in team satisfaction scores within 2 months
• **Project Delivery:** Reduced project delivery time by 25% through better collaboration
• **Communication:** Decreased miscommunication incidents by 70% through structured processes
• **Retention:** Prevented potential resignation of 2 key team members who were considering leaving
• **Productivity:** Increased team velocity by 30% as measured by completed story points
• **Leadership Growth:** Developed stronger conflict resolution skills that benefited future team management"""
            
        elif 'deadline' in original_lower or 'time' in original_lower:
            return """We successfully met the compressed timeline with excellent results:

• **On-Time Delivery:** Completed the project 2 days ahead of the revised 3-week deadline
• **Quality Maintained:** Achieved 98% defect-free delivery despite the accelerated schedule
• **Cost Efficiency:** Delivered under budget by 15% through optimized resource allocation
• **Client Satisfaction:** Received 9.5/10 satisfaction rating from the client for both quality and speed
• **Team Learning:** Established new rapid-delivery processes now used across the organization
• **Future Impact:** Created a reusable framework that reduced similar project timelines by 40%"""
            
        else:
            return """The comprehensive approach yielded measurable success:

• **Primary Objective:** Successfully resolved the core challenge within the designated timeframe
• **Performance Metrics:** Achieved 95% of established success criteria and KPIs
• **Stakeholder Satisfaction:** Received positive feedback from 100% of key stakeholders
• **Process Innovation:** Developed new methodologies that improved efficiency by 30%
• **Cost Effectiveness:** Delivered solution 20% under projected budget through strategic resource management
• **Long-term Impact:** Created sustainable improvements that continue to benefit the organization"""
            
    except Exception:
        return "Successfully achieved all primary objectives, improved key performance metrics by 30%, received positive stakeholder feedback, and created lasting improvements for the organization."

def _enhance_strong_response(response: str) -> str:
    """Minor enhancements for already strong responses"""
    # Add professional polish and ensure metrics are highlighted
    enhanced = response.strip()
    
    # Add section headers if not present
    if not any(keyword in enhanced.lower() for keyword in ['situation:', 'task:', 'action:', 'result:']):
        # Try to identify natural breaks and add headers
        sentences = enhanced.split('. ')
        if len(sentences) >= 4:
            # Simple heuristic to add STAR structure
            enhanced = f"**Situation:** {sentences[0]}.\n\n**Task:** {sentences[1]}.\n\n**Action:** {'. '.join(sentences[2:-1])}.\n\n**Result:** {sentences[-1]}"
    
    return enhanced

def _generate_follow_ups(question: str, response: str) -> List[str]:
    """
    Generate 3-5 realistic recruiter follow-up questions
    """
    # Base follow-ups that work for most scenarios
    follow_ups = [
        "What specific challenges did you encounter during this process, and how did you overcome them?",
        "How did you measure the success of your solution, and what metrics did you track?",
        "If you had to approach this situation again, what would you do differently?",
        "How did this experience influence your approach to similar challenges in the future?",
        "What feedback did you receive from stakeholders, and how did you incorporate it?"
    ]
    
    # Add question-specific follow-ups based on keywords
    question_lower = question.lower()
    
    if 'team' in question_lower or 'leadership' in question_lower:
        follow_ups.append("How did you handle any resistance or conflicting opinions within the team?")
        follow_ups.append("What strategies did you use to motivate and align team members?")
    
    if 'deadline' in question_lower or 'time' in question_lower:
        follow_ups.append("How did you prioritize tasks when time was limited?")
        follow_ups.append("What contingency plans did you have in place if deadlines were missed?")
    
    if 'technical' in question_lower or 'problem' in question_lower:
        follow_ups.append("What tools or technologies did you leverage to solve this problem?")
        follow_ups.append("How did you ensure the technical solution was scalable and maintainable?")
    
    # Return 4-5 most relevant follow-ups
    return follow_ups[:5]

# Test functions
def test_rewrite_functionality():
    """Test the rewriting functionality with various response strengths"""
    test_cases = [
        {
            'question': "Tell me about a time you solved a difficult technical problem",
            'weak_response': "I fixed a bug in our website",
            'expected_improvement': True
        },
        {
            'question': "Describe a time you led a team through a challenge",
            'medium_response': "When I was team lead, we had a project deadline issue. I organized meetings and we delivered on time.",
            'expected_improvement': True  
        },
        {
            'question': "Tell me about a time you improved a process",
            'strong_response': "At TechCorp, our deployment process was taking 4 hours and causing frequent downtime. I was tasked with reducing deployment time and improving reliability. I analyzed our current pipeline, identified bottlenecks, and implemented automated testing and blue-green deployments. This reduced deployment time to 30 minutes and decreased downtime incidents by 85%.",
            'expected_improvement': False
        }
    ]
    
    print("Testing Rewrite Functionality:")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        question = test_case['question']
        response_key = [k for k in test_case.keys() if 'response' in k and k != 'expected_improvement'][0]
        response = test_case[response_key]
        
        print(f"\nTest Case {i}: {response_key.replace('_', ' ').title()}")
        print(f"Question: {question}")
        print(f"Original: {response}")
        
        # Get original score
        original_score = score_star(response)
        print(f"Original STAR Score: {original_score['total_score']}/8")
        
        # Get rewrite
        rewrite_result = rewrite_response(question, response)
        print(f"Rewritten Response:\n{rewrite_result['rewritten_response']}")
        
        # Score the rewritten response
        new_score = score_star(rewrite_result['rewritten_response'])
        print(f"New STAR Score: {new_score['total_score']}/8")
        print(f"Improvement: +{new_score['total_score'] - original_score['total_score']} points")
        
        print(f"Sample Follow-ups:")
        for j, follow_up in enumerate(rewrite_result['follow_up_questions'][:3], 1):
            print(f"  {j}. {follow_up}")
        
        print("-" * 30)

# Test function
if __name__ == "__main__":
    print("Testing STAR Evaluation:")
    test_response = "I fixed a bug in our website"
    result = score_star(test_response)
    print("Test Result:", result)
    print("\n" + "="*50)
    
    print("Testing Response Rewriting:")
    rewrite_result = rewrite_response(
        "Tell me about a time you solved a technical problem", 
        test_response
    )
    print("Rewrite Result:")
    print(rewrite_result['rewritten_response'])
    print("\nFollow-up Questions:")
    for i, q in enumerate(rewrite_result['follow_up_questions'], 1):
        print(f"{i}. {q}")
    
    print("\n" + "="*50)
    # Run comprehensive tests
    test_rewrite_functionality()