"""
AI Study Companion - Interview Mentor
Streamlit application for STAR methodology feedback
"""

import streamlit as st
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from star_rubric import score_star, rewrite_response
except ImportError:
    st.error("❌ Could not import STAR evaluation functions. Please check the src/star_rubric.py file.")
    st.stop()

def main():
    st.title("🎯 AI Study Companion - Interview Mentor")
    st.markdown("**STAR Methodology Interview Feedback Tool**")
    st.markdown("---")
    
    # Initialize session state at the very beginning
    if 'evaluation_result' not in st.session_state:
        st.session_state.evaluation_result = None
    if 'evaluated_response' not in st.session_state:
        st.session_state.evaluated_response = ""
    if 'evaluated_question' not in st.session_state:
        st.session_state.evaluated_question = ""
    if 'custom_questions' not in st.session_state:
        st.session_state.custom_questions = []
    if 'rewrite_result' not in st.session_state:
        st.session_state.rewrite_result = None
    
    # Debug option (remove in production)
    with st.expander("🔧 Debug Options", expanded=False):
        if st.button("🗑️ Clear All Cache & Session State"):
            st.cache_data.clear()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ All cache and session state cleared!")
            st.rerun()
    
    # Sidebar for question selection
    with st.sidebar:
        st.header("📄 Question Bank")
        
        # Question input method selection
        question_method = st.radio(
            "How would you like to select a question?",
            options=["📋 Choose from samples", "✍️ Enter custom question", "📄 Upload PDF (Coming Soon)"],
            help="Choose your preferred method for selecting interview questions"
        )
        
        selected_question = None
        
        if question_method == "📋 Choose from samples":
            # Sample questions
            st.subheader("Sample Questions")
            sample_questions = [
                "Tell me about a time you had to solve a difficult problem",
                "Describe a situation where you had to work with a difficult team member", 
                "Give an example of a time you had to meet a tight deadline",
                "Tell me about a time you had to learn something new quickly",
                "Describe a situation where you had to lead a project",
                "Tell me about a time you had to handle a conflict at work",
                "Describe a challenging goal you set and how you achieved it",
                "Give an example of when you had to adapt to a significant change",
                "Tell me about a time you made a mistake and how you handled it",
                "Describe a situation where you had to influence others without authority"
            ]
            
            # Remove duplicates and ensure clean list
            sample_questions = list(dict.fromkeys(sample_questions))  # Remove duplicates while preserving order
            
            # Create fresh options list without any caching issues
            dropdown_options = ["-- Select a question --"]
            dropdown_options.extend(sample_questions)
            
            selected_question = st.selectbox(
                "Choose a question:",
                options=dropdown_options,
                help="Select from our curated list of common interview questions"
            )
            
        elif question_method == "✍️ Enter custom question":
            # Custom question input
            st.subheader("Custom Question")
            custom_question = st.text_area(
                "Enter your interview question:",
                placeholder="Type your own interview question here...\n\nExample: Tell me about a time when you had to work under pressure to deliver a project on time.",
                height=100,
                help="Enter any behavioral or technical interview question you'd like to practice"
            )
            
            if custom_question.strip():
                selected_question = custom_question.strip()
                
                # Add button to save custom question
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("💾 Save Question", help="Save this question for future use"):
                        if selected_question not in st.session_state.custom_questions:
                            st.session_state.custom_questions.append(selected_question)
                            st.success("✅ Question saved!")
                        else:
                            st.info("ℹ️ Question already saved")
                
                with col2:
                    st.success(f"✅ Custom question ready!")
            else:
                st.info("👆 Enter a question above to get started")
            
            # Show saved custom questions
            if st.session_state.custom_questions:
                st.subheader("📚 Your Saved Questions")
                saved_question_choice = st.selectbox(
                    "Select from your saved questions:",
                    options=["Choose a saved question..."] + [f"{q[:60]}{'...' if len(q) > 60 else ''}" for q in st.session_state.custom_questions],
                    help="Select from questions you've previously saved"
                )
                
                if saved_question_choice and saved_question_choice != "Choose a saved question...":
                    # Find the full question text
                    for i, saved_q in enumerate(st.session_state.custom_questions):
                        if saved_question_choice.startswith(saved_q[:60]):
                            selected_question = saved_q
                            break
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.success(f"✅ Selected saved question")
                    with col2:
                        if st.button("🗑️ Delete", help="Delete this saved question"):
                            # Find and remove the question
                            for i, saved_q in enumerate(st.session_state.custom_questions):
                                if saved_question_choice.startswith(saved_q[:60]):
                                    st.session_state.custom_questions.pop(i)
                                    st.rerun()
                                    break
                
        else:  # PDF Upload (Coming Soon)
            st.subheader("PDF Upload")
            st.info("📄 PDF upload feature coming soon!")
            st.markdown("""
            **Coming Features:**
            - Upload your company's interview question bank
            - Extract questions automatically from PDFs
            - Categorize questions by type (behavioral, technical, etc.)
            - Search and filter questions
            """)
        
        # Question category helper (for all methods)
        if selected_question and selected_question not in ["Select a question...", "-- Choose a question --", "-- Select a question --"]:
            st.markdown("---")
            st.subheader("💡 Question Analysis")
            
            # Analyze question type
            question_lower = selected_question.lower()
            question_types = []
            
            if any(word in question_lower for word in ['team', 'conflict', 'difficult person', 'leadership', 'lead']):
                question_types.append("👥 Leadership/Teamwork")
            if any(word in question_lower for word in ['problem', 'challenge', 'difficult', 'issue']):
                question_types.append("🔧 Problem-Solving")
            if any(word in question_lower for word in ['deadline', 'pressure', 'time', 'urgent']):
                question_types.append("⏰ Time Management")
            if any(word in question_lower for word in ['change', 'adapt', 'new', 'learn']):
                question_types.append("🔄 Adaptability")
            if any(word in question_lower for word in ['mistake', 'failure', 'wrong', 'error']):
                question_types.append("📚 Learning from Failure")
            
            if question_types:
                st.write("**Question Type(s):**")
                for qtype in question_types:
                    st.write(f"• {qtype}")
            else:
                st.write("**Question Type:** 🎯 General Behavioral")
            
            # STAR reminder specific to question type
            st.write("**STAR Focus Areas:**")
            if "👥 Leadership/Teamwork" in question_types:
                st.write("• **Situation**: Team context, roles, dynamics")
                st.write("• **Task**: Your leadership responsibility")
                st.write("• **Action**: How you influenced/managed people")
                st.write("• **Result**: Team performance, relationships improved")
            elif "🔧 Problem-Solving" in question_types:
                st.write("• **Situation**: What was broken/challenging")
                st.write("• **Task**: Your role in solving it")
                st.write("• **Action**: Analysis steps, solution approach")
                st.write("• **Result**: Problem resolved, metrics improved")
            elif "⏰ Time Management" in question_types:
                st.write("• **Situation**: Time constraints, competing priorities")
                st.write("• **Task**: What needed to be delivered when")
                st.write("• **Action**: How you organized/prioritized")
                st.write("• **Result**: Met deadline, quality maintained")
            else:
                st.write("• **Situation**: Context and background")
                st.write("• **Task**: Your specific responsibility")
                st.write("• **Action**: What you did (be specific)")
                st.write("• **Result**: Outcome with numbers/impact")
    
    # Main area
    if selected_question and selected_question not in ["Select a question...", "-- Choose a question --", "-- Select a question --"]:
        st.subheader("📝 Interview Question")
        st.write(f"**{selected_question}**")
        
        # Response input
        user_response = st.text_area(
            "Your Response:",
            placeholder="Type your response here using the STAR methodology (Situation, Task, Action, Result)...",
            height=200
        )
        
        # Evaluate button
        if st.button("🔍 Evaluate Response", type="primary"):
            if user_response.strip():
                # Get STAR evaluation
                with st.spinner("Analyzing your response..."):
                    st.session_state.evaluation_result = score_star(user_response)
                    st.session_state.evaluated_response = user_response
                    st.session_state.evaluated_question = selected_question
                    # Clear any previous rewrite when new evaluation is done
                    st.session_state.rewrite_result = None
            else:
                st.warning("Please enter a response to evaluate.")
        
        # Display evaluation results if available
        if st.session_state.evaluation_result is not None:
            evaluation = st.session_state.evaluation_result
            
            # Display results
            st.markdown("---")
            st.subheader("📊 STAR Evaluation Results")
            
            # Score overview
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Situation", f"{evaluation['situation']['score']}/2")
            with col2:
                st.metric("Task", f"{evaluation['task']['score']}/2")
            with col3:
                st.metric("Action", f"{evaluation['action']['score']}/2")
            with col4:
                st.metric("Result", f"{evaluation['result']['score']}/2")
            with col5:
                st.metric("Total Score", f"{evaluation['total_score']}/8")
            
            # Detailed feedback
            st.subheader("💡 Detailed Feedback")
            
            feedback_items = [
                ("🎬 Situation", evaluation['situation']),
                ("🎯 Task", evaluation['task']),
                ("⚡ Action", evaluation['action']),
                ("🏆 Result", evaluation['result'])
            ]
            
            for label, item in feedback_items:
                score = item['score']
                feedback = item['feedback']
                
                # Color coding based on score
                if score == 2:
                    st.success(f"**{label}** (Score: {score}/2)")
                    st.write(feedback)
                elif score == 1:
                    st.warning(f"**{label}** (Score: {score}/2)")
                    st.write(feedback)
                else:
                    st.error(f"**{label}** (Score: {score}/2)")
                    st.write(feedback)
            
            # Suggestions
            if evaluation['suggestions']:
                st.subheader("🔧 Improvement Suggestions")
                for suggestion in evaluation['suggestions']:
                    st.write(f"• {suggestion}")
                
            # Response Rewriting Section
            st.markdown("---")
            st.subheader("✨ AI-Enhanced Response")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("🚀 Generate Improved Response", type="secondary"):
                    with st.spinner("Rewriting your response using STAR methodology..."):
                        try:
                            # Use the stored evaluated response and question
                            st.session_state.rewrite_result = rewrite_response(
                                st.session_state.evaluated_question, 
                                st.session_state.evaluated_response
                            )
                            st.success("✅ Response enhanced!")
                        except Exception as e:
                            st.error(f"❌ Error generating rewrite: {str(e)}")
                            st.session_state.rewrite_result = None
            
            with col2:
                if st.button("🗑️ Clear Enhanced Response"):
                    st.session_state.rewrite_result = None
                    st.success("✅ Cleared enhanced response")
                
                # Display rewrite results if available
                if st.session_state.rewrite_result is not None:
                    rewrite_result = st.session_state.rewrite_result
                    
                    # Display improvement notes
                    st.info(f"**Improvement Notes:** {rewrite_result['improvement_notes']}")
                    
                    # Display rewritten response
                    st.text_area(
                        "Enhanced STAR Response (90-second target):",
                        value=rewrite_result['rewritten_response'],
                        height=300,
                        help="This is an AI-enhanced version of your response following STAR methodology",
                        key="rewritten_response_display"
                    )
                    
                    # Display follow-up questions
                    st.subheader("🤔 Potential Follow-up Questions")
                    st.write("*Recruiters might ask these follow-up questions:*")
                    for i, question in enumerate(rewrite_result['follow_up_questions'], 1):
                        st.write(f"{i}. {question}")
                        
                    # Score the enhanced response
                    enhanced_evaluation = score_star(rewrite_result['rewritten_response'])
                    st.subheader("📈 Enhanced Response Score")
                    
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col1:
                        st.metric("Original Score", f"{evaluation['total_score']}/8")
                    with col2:
                        st.metric("Enhanced Score", f"{enhanced_evaluation['total_score']}/8")
                    with col3:
                        improvement = enhanced_evaluation['total_score'] - evaluation['total_score']
                        st.metric("Improvement", f"+{improvement} points", delta=improvement)
                else:
                    st.info("👆 Click 'Generate Improved Response' to see an AI-enhanced version of your answer using STAR methodology.")
                
                # Export functionality
                st.markdown("---")
                st.subheader("📄 Export Session")
                
                if st.button("📄 Export Session", type="primary"):
                    # Determine question source
                    question_source = "Custom Question" if question_method == "✍️ Enter custom question" else "Sample Question"
                    
                    # Prepare export data
                    export_data = {
                        "question": selected_question,
                        "question_source": question_source,
                        "question_method": question_method,
                        "original_response": user_response,
                        "original_evaluation": evaluation,
                        "enhanced_response": st.session_state.rewrite_result['rewritten_response'] if st.session_state.rewrite_result else None,
                        "enhanced_evaluation": score_star(st.session_state.rewrite_result['rewritten_response']) if st.session_state.rewrite_result else None,
                        "follow_up_questions": st.session_state.rewrite_result['follow_up_questions'] if st.session_state.rewrite_result else [],
                        "improvement_notes": st.session_state.rewrite_result['improvement_notes'] if st.session_state.rewrite_result else None,
                        "session_timestamp": str(st.session_state.get('session_timestamp', 'Not available'))
                    }
                    
                    # Create formatted export text
                    export_text = f"""AI Study Companion - Interview Session Report
{'='*50}

QUESTION SOURCE: {question_source}
QUESTION:
{selected_question}

ORIGINAL RESPONSE:
{user_response}

ORIGINAL STAR EVALUATION:
• Situation: {evaluation['situation']['score']}/2 - {evaluation['situation']['feedback']}
• Task: {evaluation['task']['score']}/2 - {evaluation['task']['feedback']}
• Action: {evaluation['action']['score']}/2 - {evaluation['action']['feedback']}
• Result: {evaluation['result']['score']}/2 - {evaluation['result']['feedback']}
• Total Score: {evaluation['total_score']}/8

IMPROVEMENT SUGGESTIONS:
"""
                    for suggestion in evaluation['suggestions']:
                        export_text += f"• {suggestion}\n"
                    
                    if st.session_state.rewrite_result:
                        export_text += f"""
ENHANCED RESPONSE:
{st.session_state.rewrite_result['rewritten_response']}

ENHANCEMENT NOTES:
{st.session_state.rewrite_result['improvement_notes']}

FOLLOW-UP QUESTIONS:
"""
                        for i, q in enumerate(st.session_state.rewrite_result['follow_up_questions'], 1):
                            export_text += f"{i}. {q}\n"
                        
                        enhanced_eval = score_star(st.session_state.rewrite_result['rewritten_response'])
                        improvement = enhanced_eval['total_score'] - evaluation['total_score']
                        export_text += f"""
ENHANCED EVALUATION:
• Total Score: {enhanced_eval['total_score']}/8
• Improvement: +{improvement} points
"""
                    
                    export_text += f"""
{'='*50}
Generated by AI Study Companion - Interview Mentor
"""
                    
                    st.download_button(
                        label="📥 Download Complete Session Report",
                        data=export_text,
                        file_name=f"interview_session_{selected_question[:20].replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                    st.success("✅ Session exported successfully!")
    
    else:
        # Welcome screen
        st.markdown("""
        ## How It Works
        
        1. **📝 Select a Question** - Choose from sample interview questions (or upload your own PDF later)
        2. **✍️ Write Your Response** - Answer using the STAR methodology
        3. **🔍 Get Feedback** - Receive detailed evaluation and improvement suggestions
        4. **📄 Export Results** - Save your session for future reference
        
        ### STAR Methodology Reminder
        - **🎬 Situation**: Describe the context and background
        - **🎯 Task**: Explain your responsibility and what needed to be done
        - **⚡ Action**: Detail the specific steps you took
        - **🏆 Result**: Share the outcome and quantifiable impact
        """)
        
        # Quick test section
        st.markdown("---")
        st.subheader("🧪 Quick Test")
        st.write("Try a sample response to see how the evaluation works:")
        
        if st.button("Test with Sample Response"):
            sample_response = "When I was working at TechCorp, our main client website was down for 2 hours. I was responsible for fixing it quickly. I analyzed the server logs, identified a database connection issue, and implemented a fix by restarting the database service and updating the connection pool settings. As a result, we restored service in 30 minutes and prevented potential $50,000 in lost revenue."
            
            evaluation = score_star(sample_response)
            st.write("**Sample Response:**", sample_response)
            st.write("**Evaluation:**", evaluation)

if __name__ == "__main__":
    main()