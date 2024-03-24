def get_question_generator_prompt(question: str, context: str):
    return f'''
    Instructions: Generate three concise questions that a website visitor might ask about the company, following the context provided. Questions should be general, straightforward, and contain fewer than 10 words, reflecting a broad interest without delving into highly specific details.
    Previous Question: {question}
    Context about the company: {context}
    Example of Desired AI Behavior:
    If a customer inquires about Topo's operational mechanism, suitable questions to generate could include "What benefits does Topo offer?" "Is Topo easy to integrate?" "Who benefits most from using Topo?" These questions remain open-ended, prompt for broader information about Topo's utility, integration process, and target user base, without requiring excessively detailed or niche knowledge.
    '''
