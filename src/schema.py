SQLITE_SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS user_profile (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        native_language TEXT DEFAULT 'Portuguese',
        target_language TEXT DEFAULT 'German',
        current_level TEXT DEFAULT 'A1',
        created_at TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS lessons (
        lesson_id INTEGER PRIMARY KEY,
        module TEXT,
        title_de TEXT,
        title_pt TEXT,
        description_pt TEXT,
        level TEXT,
        order_index INTEGER,
        skill_focus TEXT,
        grammar_focus TEXT,
        vocabulary_topic TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS vocabulary (
        vocab_id INTEGER PRIMARY KEY,
        german TEXT,
        portuguese TEXT,
        article TEXT,
        plural TEXT,
        word_type TEXT,
        topic TEXT,
        level TEXT,
        example_de TEXT,
        example_pt TEXT,
        pronunciation_hint TEXT,
        difficulty INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS grammar_topics (
        grammar_id INTEGER PRIMARY KEY,
        topic_name TEXT,
        explanation_pt TEXT,
        examples_de TEXT,
        examples_pt TEXT,
        level TEXT,
        difficulty INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS exercises (
        exercise_id INTEGER PRIMARY KEY,
        lesson_id INTEGER,
        exercise_type TEXT,
        prompt_pt TEXT,
        prompt_de TEXT,
        correct_answer TEXT,
        options TEXT,
        explanation_pt TEXT,
        grammar_topic TEXT,
        vocabulary_topic TEXT,
        difficulty INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS user_attempts (
        attempt_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        exercise_id INTEGER,
        user_answer TEXT,
        correct_answer TEXT,
        is_correct BOOLEAN,
        error_type TEXT,
        grammar_topic TEXT,
        vocabulary_topic TEXT,
        time_spent_seconds INTEGER,
        created_at TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS mastery_state (
        mastery_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        topic_type TEXT,
        topic_name TEXT,
        mastery_score REAL,
        attempts INTEGER,
        correct_attempts INTEGER,
        last_practiced TIMESTAMP,
        next_review TIMESTAMP,
        UNIQUE(user_id, topic_type, topic_name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS review_queue (
        review_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        item_type TEXT,
        item_id INTEGER,
        ease_factor REAL,
        interval_days INTEGER,
        repetitions INTEGER,
        due_date TIMESTAMP,
        last_result TEXT,
        UNIQUE(user_id, item_type, item_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS translation_history (
        translation_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        source_text TEXT,
        source_language TEXT,
        target_language TEXT,
        translated_text TEXT,
        explanation_pt TEXT,
        created_at TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS speaking_attempts (
        speaking_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        prompt_text_de TEXT,
        expected_text_de TEXT,
        user_transcription TEXT,
        score REAL,
        feedback_pt TEXT,
        created_at TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS writing_attempts (
        writing_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        prompt_pt TEXT,
        user_text_de TEXT,
        corrected_text_de TEXT,
        feedback_pt TEXT,
        grammar_errors TEXT,
        vocabulary_errors TEXT,
        score REAL,
        created_at TIMESTAMP
    )
    """,
]
