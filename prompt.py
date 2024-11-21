PROMPT= """

Analyze the uploaded image and provide a detailed response based on the user's query: {input_text}.

Specifically, focus on providing the following information relevant to the query:

- Relevant object detection and description
- Scene analysis and context
- Action or event identification
- Color palette and dominant colors
- Texture and pattern recognition
- Facial feature analysis (if applicable)
- Text transcription (if applicable)
- Contextual information (time period, location, cultural references)
Format your response using clear headings, bullet points, and concise descriptions.


Or in a more concise format:

Analyze the uploaded image and provide details on {input_text}. Include relevant objects, scene, actions, colors, textures, facial features, text, and context. Respond in a structured format.

"""