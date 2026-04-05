'use client';

import { useState } from 'react';

type Scope = {
  prerequisite_concepts: string[];
  out_of_scope: string[];
};

type Concept = {
  explanation: string;
  key_points: string[];
};

type Example = {
  input: string;
  output: string;
  explanation: string;
};

type Lesson = {
  lesson_id: string;
  goal: string;
  title: string;
  scope: Scope;
  concept: Concept;
  example: Example;
  task: {
    prompt: string;
    instructions: string;
    response_type: string;
    expected_format: string;
  };
};

type Evaluation = {
  lesson_id: string;
  response_type: string;
  learner_response: string;
  score: number;
  feedback: string;
  correct: boolean;
  next_action: string;
  misconception: string | null;
};

export default function HomePage() {
  const [goal, setGoal] = useState('');
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [response, setResponse] = useState('');
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [loading, setLoading] = useState(false);

  const API = 'http://192.168.0.138:8010';

  const handleGenerate = async () => {
    setLoading(true);
    setEvaluation(null);

    const res = await fetch(`${API}/generate-lesson`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ goal }),
    });

    const data = await res.json();
    setLesson(data);
    setLoading(false);
  };

  const handleEvaluate = async () => {
    if (!lesson) return;

    setLoading(true);

    const res = await fetch(`${API}/evaluate-response`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        lesson,
        learner_response: response,
      }),
    });

    const data = await res.json();
    setEvaluation(data);
    setLoading(false);
  };

  return (
    <main style={{ padding: 40, maxWidth: 800, margin: '0 auto' }}>
      <h1>Owl of Athens</h1>

      <div>
        <h2>1. Enter Goal</h2>
        <input
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="learn python loops"
          style={{ width: '100%', padding: 10 }}
        />
        <button onClick={handleGenerate} disabled={loading}>
          Generate Lesson
        </button>
      </div>

      {lesson && (
        <div style={{ marginTop: 40 }}>
          <h2>2. Lesson</h2>
          <h3>{lesson.title}</h3>
          <p>{lesson.concept.explanation}</p>

          <pre>{lesson.example.input}</pre>
          <pre>{lesson.example.output}</pre>

          <h4>Task:</h4>
          <p>{lesson.task.prompt}</p>
          <p>
            <b>Instructions:</b> {lesson.task.instructions}
          </p>
          <p>
            <b>Expected:</b> {lesson.task.expected_format}
          </p>
        </div>
      )}

      {lesson && (
        <div style={{ marginTop: 40 }}>
          <h2>3. Your Response</h2>
          <textarea
            value={response}
            onChange={(e) => setResponse(e.target.value)}
            rows={6}
            style={{ width: '100%' }}
          />
          <button onClick={handleEvaluate} disabled={loading}>
            Submit Response
          </button>
        </div>
      )}

      {evaluation && (
        <div style={{ marginTop: 40 }}>
          <h2>4. Feedback</h2>
          <p>
            <b>Score:</b> {evaluation.score}
          </p>
          <p>
            <b>Correct:</b> {evaluation.correct ? 'Yes' : 'No'}
          </p>
          <p>
            <b>Feedback:</b> {evaluation.feedback}
          </p>
          <p>
            <b>Next Action:</b> {evaluation.next_action}
          </p>
          {evaluation.misconception && (
            <p>
              <b>Misconception:</b> {evaluation.misconception}
            </p>
          )}
        </div>
      )}
    </main>
  );
}
