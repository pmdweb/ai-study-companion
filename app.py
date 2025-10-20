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
    
    # Sidebar for PDF upload (future feature)
    with st.sidebar:
        st.header("📄 Question Bank")
        st.info("PDF upload feature coming soon!")
        
        # Sample questions for now
        st.subheader("Sample Questions")
        sample_questions = [
            "Tell me about a time you had to solve a difficult problem",
            "Describe a situation where you had to work with a difficult team member",
            "Give an example of a time you had to meet a tight deadline",
            "Tell me about a time you had to learn something new quickly",
            "Describe a situation where you had to lead a project"
        ]
        
        selected_question = st.selectbox(
            "Choose a question:",
            options=["Select a question..."] + sample_questions
        )
    
    # Main area
    if selected_question and selected_question != "Select a question...":
        st.subheader("📝 Interview Question")
        st.write(f"**{selected_question}**")
        
        # Response input
        user_response = st.text_area(
            "Your Response:",
            placeholder="Type your response here using the STAR methodology (Situation, Task, Action, Result)...",
            height=200
        )
        
        # Initialize session state for evaluation
        if 'evaluation_result' not in st.session_state:
            st.session_state.evaluation_result = None
        if 'evaluated_response' not in st.session_state:
            st.session_state.evaluated_response = ""
        if 'evaluated_question' not in st.session_state:
            st.session_state.evaluated_question = ""
        
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
            
            # Initialize session state for rewrite results
            if 'rewrite_result' not in st.session_state:
                st.session_state.rewrite_result = None
            
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
                    # Prepare export data
                    export_data = {
                        "question": selected_question,
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