# debate_manager.py

import time
from datetime import datetime
from typing import List, Dict
from config import AGENTS, DEBATE_TOPIC
from llm_interface import get_cerebras_response

class DebateManager:
    """Orchestrates a multi-agent debate and saves the transcript to a file."""
    
    def __init__(self, agents: Dict, topic: str):
        self.agents = agents
        self.agent_names = list(agents.keys())
        self.topic = topic
        self.transcript_list = [f"# Debate Topic: {self.topic}\n"]
        self.conversation_log = []

    def _add_to_transcript(self, text: str):
        """Prints text to console and adds it to the transcript list."""
        print(text)
        self.transcript_list.append(text)

    def run_opening_statements(self):
        self._add_to_transcript("\n## Round 1: Opening Statements\n")
        for name in self.agent_names:
            prompt = f"It's your turn, {name}. Please state your opening position on the topic."
            
            response = get_cerebras_response(
                model=self.agents[name]["model"],
                system_prompt=self.agents[name]["persona"],
                history=[*self.conversation_log, {"role": "user", "content": prompt}]
            )
            
            self._add_to_transcript(f"### **{name}:**\n{response}\n")
            self.conversation_log.append({"role": "user", "content": f"Statement from {name}: {response}"})
            time.sleep(10)

    def run_crossexamination(self):
        self._add_to_transcript("\n## Round 2: Cross-Examination\n")
        for i in range(len(self.agent_names)):
            asker = self.agent_names[i]
            target = self.agent_names[(i + 1) % len(self.agent_names)]
            
            prompt = f"It's your turn, {asker}. Ask a challenging, direct question to {target}."
            question = get_cerebras_response(
                model=self.agents[asker]["model"],
                system_prompt=self.agents[asker]["persona"],
                history=[*self.conversation_log, {"role": "user", "content": prompt}]
            )
            self._add_to_transcript(f"### **{asker} asks {target}:**\n{question}\n")
            self.conversation_log.append({"role": "user", "content": f"Question from {asker}: {question}"})
            time.sleep(10)
            
            answer_prompt = f"It's your turn, {target}. Answer this question: '{question}'"
            answer = get_cerebras_response(
                model=self.agents[target]["model"],
                system_prompt=self.agents[target]["persona"],
                history=[*self.conversation_log, {"role": "user", "content": answer_prompt}]
            )
            self._add_to_transcript(f"### **{target} responds:**\n{answer}\n")
            self.conversation_log.append({"role": "user", "content": f"Response from {target}: {answer}"})
            time.sleep(10)

    def run_judging(self):
        self._add_to_transcript("\n## Final Round: Judgment\n")
        full_transcript_str = "\n".join(self.transcript_list)
        
        judging_prompt = f"""
        You are now an impartial judge. Forget your previous persona completely.
        Analyze the full debate transcript below. You cannot vote for yourself.
        Based on argumentation, logic, and persuasiveness, which participant performed best?
        Announce the winner's name and justify your vote in a short paragraph.
        
        Full Debate Transcript:
        {full_transcript_str}
        """
        
        for name in self.agent_names:
            neutral_system_prompt = "You are a fair and impartial judge analyzing a debate."
            vote = get_cerebras_response(
                model=self.agents[name]["model"],
                system_prompt=neutral_system_prompt,
                history=[{"role": "user", "content": judging_prompt}]
            )
            self._add_to_transcript(f"### **Vote from {name}:**\n{vote}\n")
            time.sleep(10)

    def get_full_transcript(self) -> str:
        """Joins the list of transcript entries into a single string."""
        return "\n".join(self.transcript_list)

    def start(self):
        """Starts and runs the entire debate process."""
        print("="*20)
        print(self.transcript_list[0])
        print("="*20)

        self.run_opening_statements()
        self.run_crossexamination()
        self.run_judging()
        
        self._add_to_transcript("\n---\n*The Debate has Concluded.*")

def save_transcript_to_markdown(transcript: str, filename: str = None):
    """Saves the final transcript to a Markdown file."""
    if filename is None:
        # Create a unique filename based on the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debate_transcript_{timestamp}.md"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"\n✅ Transcript successfully saved to: {filename}")
    except IOError as e:
        print(f"\n❌ Error saving file: {e}")

if __name__ == "__main__":
    debate = DebateManager(AGENTS, DEBATE_TOPIC)
    debate.start()
    
    # After the debate is finished, get the full transcript and save it.
    final_transcript = debate.get_full_transcript()
    save_transcript_to_markdown(final_transcript)