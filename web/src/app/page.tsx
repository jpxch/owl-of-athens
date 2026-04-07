'use client';

import { useState } from 'react';
import styles from './page.module.scss';

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

type RequestState = 'idle' | 'generating' | 'evaluating';

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, '') ?? 'http://localhost:8010';

const NEXT_ACTION_LABELS: Record<string, string> = {
  continue: 'Continue forward',
  retry: 'Try this lesson again',
  review: 'Review the concept first',
};

const EXAMPLE_GOALS = [
  'Learn Python loops',
  'Understand SQL joins',
  'Practice writing clear commit messages',
];

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function isLesson(payload: unknown): payload is Lesson {
  return (
    isRecord(payload) &&
    typeof payload.lesson_id === 'string' &&
    typeof payload.goal === 'string' &&
    typeof payload.title === 'string' &&
    isRecord(payload.task) &&
    typeof payload.task.prompt === 'string'
  );
}

function isEvaluation(payload: unknown): payload is Evaluation {
  return (
    isRecord(payload) &&
    typeof payload.lesson_id === 'string' &&
    typeof payload.feedback === 'string' &&
    typeof payload.score === 'number' &&
    typeof payload.correct === 'boolean'
  );
}

async function parseApiPayload(response: Response): Promise<unknown> {
  const raw = await response.text();

  if (!raw.trim()) {
    return null;
  }

  try {
    return JSON.parse(raw) as unknown;
  } catch {
    throw new Error('The server returned invalid JSON. Please try again.');
  }
}

function getApiErrorMessage(payload: unknown, fallback: string): string {
  if (!isRecord(payload)) {
    return fallback;
  }

  const detail = payload.detail;
  if (typeof payload.detail === 'string' && payload.detail.trim()) {
    return payload.detail;
  }

  if (
    isRecord(detail) &&
    typeof detail.message === 'string' &&
    detail.message.trim()
  ) {
    return detail.message;
  }

  const error = isRecord(payload.error) ? payload.error : null;

  if (error?.type === 'provider_schema_error') {
    return 'The model returned malformed data. Please try again.';
  }

  if (error?.type === 'provider_response_error') {
    return 'The model response could not be parsed. Please try again.';
  }

  return fallback;
}

export default function HomePage() {
  const [goal, setGoal] = useState('');
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [response, setResponse] = useState('');
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [requestState, setRequestState] = useState<RequestState>('idle');
  const [error, setError] = useState<string | null>(null);
  const trimmedGoal = goal.trim();
  const trimmedResponse = response.trim();
  const isGenerating = requestState === 'generating';
  const isEvaluating = requestState === 'evaluating';
  const isBusy = requestState !== 'idle';

  const handleGenerate = async () => {
    if (!trimmedGoal) {
      setError('Enter a learning goal before generating a lesson.');
      return;
    }

    setRequestState('generating');
    setLesson(null);
    setResponse('');
    setEvaluation(null);
    setError(null);

    try {
      const res = await fetch(`${API_BASE_URL}/generate-lesson`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal: trimmedGoal }),
      });

      const data = await parseApiPayload(res);

      if (!res.ok) {
        throw new Error(getApiErrorMessage(data, 'Unable to generate lesson.'));
      }

      if (!isLesson(data)) {
        throw new Error('The API returned an unexpected lesson payload.');
      }

      setLesson(data);
    } catch (err) {
      setLesson(null);
      setError(err instanceof Error ? err.message : 'Unable to generate lesson.');
    } finally {
      setRequestState('idle');
    }
  };

  const handleEvaluate = async () => {
    if (!lesson) return;
    if (!trimmedResponse) {
      setError('Write a response before requesting evaluation.');
      return;
    }

    setRequestState('evaluating');
    setError(null);

    try {
      const res = await fetch(`${API_BASE_URL}/evaluate-response`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lesson,
          learner_response: trimmedResponse,
        }),
      });

      const data = await parseApiPayload(res);

      if (!res.ok) {
        throw new Error(getApiErrorMessage(data, 'Unable to evaluate response.'));
      }

      if (!isEvaluation(data)) {
        throw new Error('The API returned an unexpected evaluation payload.');
      }

      setEvaluation(data);
    } catch (err) {
      setEvaluation(null);
      setError(err instanceof Error ? err.message : 'Unable to evaluate response.');
    } finally {
      setRequestState('idle');
    }
  };

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <section className={styles.hero}>
          <div className={styles.heroTop}>
            <span className={styles.eyebrow}>Local-first teaching loop</span>
            <div className={styles.heroMeta}>
              <span className={styles.metaPill}>Goal</span>
              <span className={styles.metaPill}>Lesson</span>
              <span className={styles.metaPill}>Response</span>
              <span className={styles.metaPill}>Evaluation</span>
            </div>
          </div>
          <h1>Owl of Athens</h1>
          <p>
            Build one sharp lesson at a time. Enter a goal, receive a structured teaching
            step, respond in the expected format, and get feedback that tells you whether
            to continue, retry, or review.
          </p>
        </section>

        <div className={styles.grid}>
          <div className={styles.stack}>
            <section className={styles.panel}>
              <div className={styles.panelHeader}>
                <span className={styles.step}>Step 1</span>
                <h2>Set the learning goal</h2>
                <p>Keep it specific enough that the system can teach one concrete step.</p>
              </div>

              <div className={styles.field}>
                <label htmlFor="goal">Learning goal</label>
                <input
                  id="goal"
                  className={styles.input}
                  value={goal}
                  onChange={(e) => {
                    setGoal(e.target.value);
                    if (error) {
                      setError(null);
                    }
                  }}
                  placeholder="Learn Python loops"
                />
                <p className={styles.fieldHint}>
                  Aim for one teachable step, not an entire subject.
                </p>
              </div>

              <div className={styles.examples}>
                <span className={styles.examplesLabel}>Try a starter goal</span>
                <div className={styles.exampleList}>
                  {EXAMPLE_GOALS.map((exampleGoal) => (
                    <button
                      key={exampleGoal}
                      className={styles.exampleChip}
                      type="button"
                      onClick={() => {
                        setGoal(exampleGoal);
                        setError(null);
                      }}
                      disabled={isBusy}
                    >
                      {exampleGoal}
                    </button>
                  ))}
                </div>
              </div>

              <div className={styles.buttonRow}>
                <button
                  className={styles.button}
                  onClick={handleGenerate}
                  disabled={isBusy || trimmedGoal.length === 0}
                >
                  {isGenerating ? 'Generating lesson...' : 'Generate lesson'}
                </button>
              </div>

              {error && (
                <div className={styles.alert} role="alert">
                  <strong>Error:</strong> {error}
                </div>
              )}
            </section>

            {lesson && (
              <section className={styles.panel}>
                <div className={styles.panelHeader}>
                  <span className={styles.step}>Step 2</span>
                  <h2>{lesson.title}</h2>
                  <p>{lesson.concept.explanation}</p>
                </div>

                <div className={styles.summary}>
                  <article className={styles.summaryCard}>
                    <span className={styles.summaryLabel}>Scope</span>
                    <div className={styles.inlineGrid}>
                      <div>
                        <h3>Prerequisites</h3>
                        <ul>
                          {lesson.scope.prerequisite_concepts.map((item) => (
                            <li key={item}>{item}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h3>Out of scope</h3>
                        <ul>
                          {lesson.scope.out_of_scope.map((item) => (
                            <li key={item}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </article>

                  <article className={styles.summaryCard}>
                    <span className={styles.summaryLabel}>Key points</span>
                    <ul>
                      {lesson.concept.key_points.map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </article>

                  <article className={styles.summaryCard}>
                    <span className={styles.summaryLabel}>Worked example</span>
                    <div className={styles.inlineGrid}>
                      <div>
                        <h4>Input</h4>
                        <pre className={styles.codeBlock}>{lesson.example.input}</pre>
                      </div>
                      <div>
                        <h4>Output</h4>
                        <pre className={styles.codeBlock}>{lesson.example.output}</pre>
                      </div>
                    </div>
                    <p className={styles.muted}>{lesson.example.explanation}</p>
                  </article>

                  <article className={styles.summaryCard}>
                    <span className={styles.summaryLabel}>Task</span>
                    <h3>{lesson.task.prompt}</h3>
                    <p className={styles.muted}>{lesson.task.instructions}</p>
                    <dl className={styles.inlineGrid}>
                      <div className={styles.metric}>
                        <dt>Response type</dt>
                        <dd>{lesson.task.response_type}</dd>
                      </div>
                      <div className={styles.metric}>
                        <dt>Expected format</dt>
                        <dd>{lesson.task.expected_format}</dd>
                      </div>
                    </dl>
                  </article>
                </div>
              </section>
            )}

            {lesson && (
              <section className={styles.panel}>
                <div className={styles.panelHeader}>
                  <span className={styles.step}>Step 3</span>
                  <h2>Submit your response</h2>
                  <p>Answer in the format requested by the lesson so the evaluation is fair.</p>
                </div>

                <div className={styles.field}>
                  <label htmlFor="response">Your response</label>
                  <textarea
                    id="response"
                    className={styles.textarea}
                    value={response}
                    onChange={(e) => setResponse(e.target.value)}
                    rows={8}
                    placeholder="Write your answer here..."
                  />
                </div>

                <div className={styles.buttonRow}>
                  <button
                    className={styles.button}
                    onClick={handleEvaluate}
                    disabled={isBusy || trimmedResponse.length === 0}
                  >
                    {isEvaluating ? 'Evaluating response...' : 'Evaluate response'}
                  </button>
                  <button
                    className={`${styles.button} ${styles.ghostButton}`}
                    type="button"
                    onClick={() => setResponse('')}
                    disabled={isBusy || response.length === 0}
                  >
                    Clear response
                  </button>
                </div>
              </section>
            )}
          </div>

          <aside className={`${styles.stack} ${styles.sideRail}`}>
            <section className={styles.panel}>
              <div className={styles.panelHeader}>
                <span className={styles.step}>Workspace</span>
                <h3>Loop status</h3>
                <p>The current learner flow stays intentionally small while we harden the spine.</p>
              </div>
              <dl className={styles.summary}>
                <div className={styles.metric}>
                  <dt>Goal</dt>
                  <dd>{trimmedGoal || 'Waiting for input'}</dd>
                </div>
                <div className={styles.metric}>
                  <dt>Lesson</dt>
                  <dd>{lesson ? lesson.title : 'Not generated yet'}</dd>
                </div>
                <div className={styles.metric}>
                  <dt>Response</dt>
                  <dd>{response.trim() ? 'Drafted' : 'Not written yet'}</dd>
                </div>
                <div className={styles.metric}>
                  <dt>Feedback</dt>
                  <dd>{evaluation ? 'Available' : 'Pending evaluation'}</dd>
                </div>
              </dl>
            </section>

            {evaluation && (
              <section className={styles.panel}>
                <div className={styles.panelHeader}>
                  <span className={styles.step}>Step 4</span>
                  <h3>Evaluation</h3>
                  <p>Feedback should help the learner decide what to do next.</p>
                </div>

                <div className={styles.scoreBadge}>
                  Score {Math.round(evaluation.score * 100)}%
                </div>

                <dl className={styles.summary}>
                  <div className={styles.metric}>
                    <dt>Correct</dt>
                    <dd>{evaluation.correct ? 'Yes' : 'No'}</dd>
                  </div>
                  <div className={styles.metric}>
                    <dt>Next action</dt>
                    <dd>
                      {NEXT_ACTION_LABELS[evaluation.next_action] ?? evaluation.next_action}
                    </dd>
                  </div>
                  <div className={styles.metric}>
                    <dt>Feedback</dt>
                    <dd>{evaluation.feedback}</dd>
                  </div>
                  {evaluation.misconception && (
                    <div className={styles.metric}>
                      <dt>Misconception</dt>
                      <dd>{evaluation.misconception}</dd>
                    </div>
                  )}
                </dl>
              </section>
            )}
          </aside>
        </div>
      </div>
    </main>
  );
}
