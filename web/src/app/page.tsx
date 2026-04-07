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

type ApiErrorResponse = {
  detail?: string | { message?: string };
  error?: {
    type?: string;
    source?: string;
    retryable?: boolean;
  };
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, '') ?? 'http://localhost:8010';

const NEXT_ACTION_LABELS: Record<string, string> = {
  continue: 'Continue forward',
  retry: 'Try this lesson again',
  review: 'Review the concept first',
};

function getApiErrorMessage(payload: ApiErrorResponse, fallback: string): string {
  if (typeof payload.detail === 'string' && payload.detail.trim()) {
    return payload.detail;
  }

  if (
    payload.detail &&
    typeof payload.detail === 'object' &&
    typeof payload.detail.message === 'string' &&
    payload.detail.message.trim()
  ) {
    return payload.detail.message;
  }

  if (payload.error?.type === 'provider_schema_error') {
    return 'The model returned malformed data. Please try again.';
  }

  if (payload.error?.type === 'provider_response_error') {
    return 'The model response could not be parsed. Please try again.';
  }

  return fallback;
}

export default function HomePage() {
  const [goal, setGoal] = useState('');
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [response, setResponse] = useState('');
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    setEvaluation(null);
    setError(null);

    try {
      const res = await fetch(`${API_BASE_URL}/generate-lesson`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal }),
      });

      const data: Lesson | ApiErrorResponse = await res.json();

      if (!res.ok) {
        throw new Error(getApiErrorMessage(data, 'Unable to generate lesson.'));
      }

      setLesson(data as Lesson);
      setResponse('');
    } catch (err) {
      setLesson(null);
      setError(err instanceof Error ? err.message : 'Unable to generate lesson.');
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluate = async () => {
    if (!lesson) return;

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE_URL}/evaluate-response`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lesson,
          learner_response: response,
        }),
      });

      const data: Evaluation | ApiErrorResponse = await res.json();

      if (!res.ok) {
        throw new Error(getApiErrorMessage(data, 'Unable to evaluate response.'));
      }

      setEvaluation(data as Evaluation);
    } catch (err) {
      setEvaluation(null);
      setError(err instanceof Error ? err.message : 'Unable to evaluate response.');
    } finally {
      setLoading(false);
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
                  onChange={(e) => setGoal(e.target.value)}
                  placeholder="Learn Python loops"
                />
              </div>

              <div className={styles.buttonRow}>
                <button className={styles.button} onClick={handleGenerate} disabled={loading}>
                  {loading ? 'Generating lesson...' : 'Generate lesson'}
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
                  <button className={styles.button} onClick={handleEvaluate} disabled={loading}>
                    {loading ? 'Evaluating response...' : 'Evaluate response'}
                  </button>
                  <button
                    className={`${styles.button} ${styles.ghostButton}`}
                    type="button"
                    onClick={() => setResponse('')}
                    disabled={loading || response.length === 0}
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
                  <dd>{goal.trim() || 'Waiting for input'}</dd>
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
