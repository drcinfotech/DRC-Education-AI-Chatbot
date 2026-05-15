import { useState } from "react";
import {
  BookOpen, Calendar, CheckCircle2, Circle, Clock, GraduationCap,
  Info, AlertTriangle, ChevronRight, Award, FileText, BarChart3,
  Coins, Lightbulb, Brain, RotateCcw, User, MapPin, AlertCircle,
  Hash, Target, Sparkles, Layers, BookMarked, Pencil, Beaker,
  ShieldCheck,
} from "lucide-react";

const ACCENT = "#A78BFA";

const fmt0 = (n) => "₹" + Math.abs(Number(n)).toLocaleString("en-IN", { maximumFractionDigits: 0 });

const STATUS_META = {
  not_started: { label: "Not started", color: "rgba(255,255,255,0.5)" },
  in_progress: { label: "In progress", color: ACCENT },
  draft:       { label: "Draft",       color: "#fde047" },
  submitted:   { label: "Submitted",   color: "#86efac" },
  graded:      { label: "Graded",      color: "#86efac" },
};

const LETTER_COLOR = (letter) => {
  if (letter.startsWith("A")) return "#86efac";
  if (letter.startsWith("B")) return ACCENT;
  if (letter.startsWith("C")) return "#fde047";
  return "#fca5a5";
};

/* ─── TextBlock ────────────────────────────────────────── */
export function TextBlock({ content }) {
  const parts = content.split(/(\*\*[^*]+\*\*)/g);
  return (
    <div
      className="text-sm leading-relaxed px-4 py-2.5 rounded-2xl rounded-tl-md"
      style={{ background: "rgba(255,255,255,0.03)", color: "rgba(255,255,255,0.88)" }}
    >
      {parts.map((p, i) =>
        p.startsWith("**") && p.endsWith("**") ? (
          <strong key={i} className="text-white font-medium">{p.slice(2, -2)}</strong>
        ) : (
          <span key={i}>{p.split("\n").map((line, j, arr) => (
            <span key={j}>{line}{j < arr.length - 1 && <br />}</span>
          ))}</span>
        )
      )}
    </div>
  );
}

/* ─── DisclaimerBlock ──────────────────────────────────── */
export function DisclaimerBlock({ content }) {
  return (
    <div
      className="flex items-start gap-2.5 px-4 py-2.5 rounded-2xl border"
      style={{ background: "rgba(250, 204, 21, 0.04)", borderColor: "rgba(250, 204, 21, 0.18)", color: "rgba(250, 204, 21, 0.85)" }}
    >
      <Info size={14} className="mt-0.5 flex-shrink-0" />
      <div className="text-11 leading-relaxed">{content}</div>
    </div>
  );
}

/* ─── IntegrityAlertBlock (integrity / privacy / social-eng) ─── */
export function IntegrityAlertBlock({ headline, message, indicators, offer }) {
  return (
    <div
      className="rounded-2xl border-2 p-4 integrity-pulse"
      style={{
        background: "linear-gradient(180deg, rgba(167,139,250,0.10), rgba(167,139,250,0.02))",
        borderColor: "rgba(167,139,250,0.4)",
      }}
    >
      <div className="flex items-center gap-2 mb-2">
        <ShieldCheck size={18} style={{ color: ACCENT }} />
        <div className="text-sm font-semibold" style={{ color: ACCENT }}>{headline}</div>
      </div>
      <div className="text-xs leading-relaxed mb-3" style={{ color: "rgba(255,255,255,0.85)" }}>{message}</div>
      <div className="space-y-1 mb-3">
        {indicators.map((it, i) => (
          <div key={i} className="flex items-start gap-2 text-11" style={{ color: "rgba(255,255,255,0.7)" }}>
            <AlertTriangle size={10} style={{ color: ACCENT, marginTop: 3, flexShrink: 0 }} />
            <span>{it}</span>
          </div>
        ))}
      </div>
      <div
        className="flex items-start gap-2 px-3 py-2 rounded-lg border"
        style={{ background: "rgba(255,255,255,0.04)", borderColor: ACCENT + "33" }}
      >
        <Lightbulb size={12} style={{ color: ACCENT, marginTop: 2, flexShrink: 0 }} />
        <div className="text-11 leading-relaxed" style={{ color: "rgba(255,255,255,0.9)" }}>{offer}</div>
      </div>
    </div>
  );
}

/* ─── ProfileBlock ─────────────────────────────────────── */
export function ProfileBlock({ student: s }) {
  return (
    <div className="rounded-xl border p-4"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-start gap-3">
        <div className="rounded-xl flex items-center justify-center flex-shrink-0 font-serif text-base"
          style={{ width: 56, height: 56, background: ACCENT + "22", color: ACCENT, border: `2px solid ${ACCENT}44` }}>
          {s.name.split(" ").map(w => w[0]).join("").slice(0, 2)}
        </div>
        <div className="flex-1">
          <div className="text-base font-medium" style={{ color: "white" }}>{s.name}</div>
          <div className="text-11" style={{ color: "rgba(255,255,255,0.6)" }}>{s.grade} · {s.section}</div>
          <div className="text-10 font-mono mt-0.5" style={{ color: "rgba(255,255,255,0.45)" }}>{s.id}</div>
        </div>
        <div className="text-right">
          <div className="text-base font-mono font-medium" style={{ color: ACCENT }}>{s.gpa}</div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>GPA</div>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-2 mt-3 pt-3 border-t" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div>
          <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>School</div>
          <div className="text-xs" style={{ color: "rgba(255,255,255,0.85)" }}>{s.school}</div>
        </div>
        <div>
          <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Board · Term</div>
          <div className="text-xs" style={{ color: "rgba(255,255,255,0.85)" }}>{s.board} · {s.term}</div>
        </div>
      </div>
    </div>
  );
}

/* ─── CoursesBlock ─────────────────────────────────────── */
export function CoursesBlock({ title, items }) {
  return (
    <div className="space-y-2">
      {title && (
        <div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>
      )}
      <div className="grid grid-cols-2 gap-2">
        {items.map((c) => (
          <div key={c.id} className="rounded-xl p-3 border"
            style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
            <div className="flex items-start gap-2 mb-2">
              <div className="rounded-lg flex items-center justify-center flex-shrink-0"
                style={{ width: 32, height: 32, background: c.color + "22", color: c.color }}>
                <BookOpen size={14} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-xs font-medium" style={{ color: "white" }}>{c.name}</div>
                <div className="text-9 font-mono" style={{ color: "rgba(255,255,255,0.5)" }}>{c.code}</div>
              </div>
              <span className="text-10 font-mono font-medium px-1.5 py-0.5 rounded-md"
                style={{ background: LETTER_COLOR(c.grade_so_far) + "22", color: LETTER_COLOR(c.grade_so_far) }}>
                {c.grade_so_far}
              </span>
            </div>
            <div className="text-10" style={{ color: "rgba(255,255,255,0.55)" }}>
              <div className="flex items-center gap-1"><User size={9} /> {c.teacher}</div>
              <div className="flex items-center gap-1 mt-0.5"><Clock size={9} /> {c.schedule}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── AssignmentsBlock ─────────────────────────────────── */
export function AssignmentsBlock({ title, items }) {
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center gap-2 mb-3">
        <Pencil size={14} style={{ color: ACCENT }} />
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>
          {title || "Assignments"}
        </div>
      </div>
      <div className="space-y-2">
        {items.map((a) => {
          const meta = STATUS_META[a.status] || STATUS_META.not_started;
          const overdue = a.due_in_hours < 0;
          const dueSoon = a.due_in_hours >= 0 && a.due_in_hours <= 48;
          return (
            <div key={a.id} className="flex items-start gap-3 px-3 py-2.5 rounded-lg"
              style={{ background: overdue ? "rgba(248,113,113,0.06)" : "rgba(255,255,255,0.02)" }}>
              <div className="rounded-md flex-shrink-0"
                style={{ width: 3, alignSelf: "stretch", background: a.course_color }} />
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <div className="text-xs font-medium" style={{ color: "white" }}>{a.title}</div>
                  <span className="text-9 px-1.5 py-0.5 rounded-full font-medium uppercase tracking-tightest2"
                    style={{ background: meta.color + "22", color: meta.color }}>
                    {meta.label}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-10 mt-0.5" style={{ color: "rgba(255,255,255,0.55)" }}>
                  <span style={{ color: a.course_color }}>{a.course_name}</span>
                  <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
                  <span>{a.type}</span>
                  <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
                  <span>{a.points} pts</span>
                </div>
                <div className="flex items-center gap-1 text-10 mt-0.5"
                  style={{ color: overdue ? "#fca5a5" : (dueSoon ? "#fde047" : "rgba(255,255,255,0.6)") }}>
                  <Clock size={9} />
                  <span>{overdue ? "Overdue · " : ""}{a.due}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ─── GradesBlock ──────────────────────────────────────── */
export function GradesBlock({ title, items, average_pct }) {
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <BarChart3 size={14} style={{ color: ACCENT }} />
          <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>
            {title || "Recent grades"}
          </div>
        </div>
        <div className="text-right">
          <div className="text-sm font-mono font-medium" style={{ color: ACCENT }}>{average_pct}%</div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>average</div>
        </div>
      </div>
      <div className="space-y-1">
        {items.map((g) => (
          <div key={g.id} className="flex items-center justify-between px-3 py-2 rounded-md"
            style={{ background: "rgba(255,255,255,0.02)" }}>
            <div className="flex items-center gap-2 flex-1 min-w-0">
              <div className="rounded-full flex-shrink-0" style={{ width: 6, height: 6, background: g.course_color }} />
              <div className="min-w-0">
                <div className="text-xs" style={{ color: "rgba(255,255,255,0.9)" }}>{g.title}</div>
                <div className="text-10" style={{ color: "rgba(255,255,255,0.45)" }}>{g.course_name} · {g.date}</div>
              </div>
            </div>
            <div className="flex items-center gap-3 flex-shrink-0">
              <div className="text-right">
                <div className="text-xs font-mono" style={{ color: "white" }}>{g.score}/{g.max}</div>
                <div className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.5)" }}>{g.pct}%</div>
              </div>
              <span className="text-xs font-mono font-medium px-1.5 py-0.5 rounded-md"
                style={{ background: LETTER_COLOR(g.letter) + "22", color: LETTER_COLOR(g.letter), minWidth: 28, textAlign: "center" }}>
                {g.letter}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── AttendanceBlock ──────────────────────────────────── */
export function AttendanceBlock({ overall_pct, present_days, total_days, by_course }) {
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <CheckCircle2 size={14} style={{ color: ACCENT }} />
          <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Attendance</div>
        </div>
        <div className="text-right">
          <div className="text-base font-mono font-medium" style={{ color: ACCENT }}>{overall_pct}%</div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>{present_days}/{total_days} days</div>
        </div>
      </div>
      <div className="h-1 rounded-full overflow-hidden mb-3" style={{ background: "rgba(255,255,255,0.06)" }}>
        <div style={{ width: `${overall_pct}%`, height: "100%", background: ACCENT, borderRadius: 999 }} />
      </div>
      <div className="space-y-1.5 pt-2 border-t" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        {by_course.map((bc, i) => {
          const low = bc.pct < 85;
          return (
            <div key={i}>
              <div className="flex items-center justify-between mb-0.5">
                <div className="flex items-center gap-1.5 text-10" style={{ color: "rgba(255,255,255,0.7)" }}>
                  <div className="rounded-full" style={{ width: 6, height: 6, background: bc.course_color }} />
                  {bc.course_name}
                </div>
                <span className="text-10 font-mono" style={{ color: low ? "#fde047" : "rgba(255,255,255,0.6)" }}>{bc.pct}%</span>
              </div>
              <div className="h-0.5 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.05)" }}>
                <div style={{ width: `${bc.pct}%`, height: "100%", background: bc.course_color, borderRadius: 999 }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ─── ScheduleBlock ────────────────────────────────────── */
export function ScheduleBlock({ title, items }) {
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center gap-2 mb-3">
        <Calendar size={14} style={{ color: ACCENT }} />
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>
          {title || "Today's schedule"}
        </div>
      </div>
      <div className="space-y-1.5">
        {items.map((slot, i) => {
          const isBreak = !slot.course;
          return (
            <div key={i} className="flex items-start gap-3 px-3 py-2 rounded-md"
              style={{ background: isBreak ? "rgba(255,255,255,0.015)" : "rgba(255,255,255,0.03)" }}>
              <div className="text-10 font-mono flex-shrink-0" style={{ color: "rgba(255,255,255,0.55)", minWidth: 80 }}>
                {slot.time}
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-xs font-medium" style={{ color: isBreak ? "rgba(255,255,255,0.55)" : "white" }}>{slot.name}</div>
                {!isBreak && (
                  <div className="text-10 mt-0.5" style={{ color: "rgba(255,255,255,0.5)" }}>
                    <span className="inline-flex items-center gap-1"><MapPin size={9} /> {slot.room}</span>
                    <span style={{ color: "rgba(255,255,255,0.3)", margin: "0 6px" }}>·</span>
                    <span>{slot.teacher}</span>
                  </div>
                )}
                {slot.note !== "—" && !isBreak && (
                  <div className="text-9 mt-0.5 italic" style={{ color: ACCENT }}>{slot.note}</div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ─── FeesBlock ────────────────────────────────────────── */
export function FeesBlock({ term, total, paid, due, due_date, breakdown }) {
  const pct = (paid / total) * 100;
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Coins size={14} style={{ color: ACCENT }} />
            <span className="text-xs font-medium" style={{ color: "white" }}>{term}</span>
          </div>
          <span className="text-10 px-1.5 py-0.5 rounded-full font-medium"
            style={{ background: due > 0 ? "rgba(252,165,165,0.15)" : "rgba(134,239,172,0.15)", color: due > 0 ? "#fca5a5" : "#86efac" }}>
            {due > 0 ? `${fmt0(due)} due` : "Fully paid"}
          </span>
        </div>
        <div className="h-1.5 rounded-full overflow-hidden mb-1" style={{ background: "rgba(255,255,255,0.06)" }}>
          <div style={{ width: `${pct}%`, height: "100%", background: ACCENT, borderRadius: 999 }} />
        </div>
        <div className="flex justify-between text-10" style={{ color: "rgba(255,255,255,0.55)" }}>
          <span><span className="font-mono" style={{ color: "white" }}>{fmt0(paid)}</span> paid of {fmt0(total)}</span>
          <span>Due by <span style={{ color: "white" }}>{due_date}</span></span>
        </div>
      </div>
      <div className="px-4 py-3 space-y-1">
        {breakdown.map((b, i) => {
          const remaining = b.amount - b.paid;
          return (
            <div key={i} className="flex items-center justify-between text-xs">
              <span style={{ color: "rgba(255,255,255,0.7)" }}>{b.head}</span>
              <div className="flex items-center gap-2">
                <span className="font-mono" style={{ color: remaining > 0 ? "rgba(255,255,255,0.9)" : "rgba(255,255,255,0.4)" }}>{fmt0(b.amount)}</span>
                {remaining === 0 && (
                  <span className="text-9 px-1 py-0.5 rounded-full" style={{ background: "rgba(134,239,172,0.15)", color: "#86efac" }}>PAID</span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ─── ConceptBlock ─────────────────────────────────────── */
export function ConceptBlock({ subject, topic, summary, key_formulas, common_mistakes, next_topics }) {
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <div className="flex items-center gap-2 mb-1">
          <Brain size={14} style={{ color: ACCENT }} />
          <span className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.55)" }}>{subject}</span>
        </div>
        <div className="text-sm font-medium" style={{ color: "white" }}>{topic}</div>
      </div>
      <div className="px-4 py-3">
        <div className="text-xs leading-relaxed mb-3" style={{ color: "rgba(255,255,255,0.85)" }}>{summary}</div>

        <div className="mb-3">
          <div className="text-10 uppercase tracking-tightest2 mb-1.5" style={{ color: "rgba(255,255,255,0.45)" }}>Key formulas</div>
          <div className="space-y-1">
            {key_formulas.map((f, i) => (
              <div key={i} className="flex items-center justify-between px-2.5 py-1.5 rounded-md"
                style={{ background: "rgba(255,255,255,0.02)" }}>
                <span className="text-11" style={{ color: "rgba(255,255,255,0.7)" }}>{f.label}</span>
                <span className="text-xs font-mono" style={{ color: ACCENT }}>{f.formula}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="mb-3">
          <div className="text-10 uppercase tracking-tightest2 mb-1.5" style={{ color: "rgba(255,255,255,0.45)" }}>Common mistakes</div>
          <div className="space-y-1">
            {common_mistakes.map((m, i) => (
              <div key={i} className="flex items-start gap-2 text-11" style={{ color: "rgba(255,255,255,0.75)" }}>
                <AlertCircle size={10} style={{ color: "#fde047", marginTop: 3, flexShrink: 0 }} />
                <span>{m}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="pt-2 border-t" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
          <div className="text-10 uppercase tracking-tightest2 mb-1.5" style={{ color: "rgba(255,255,255,0.45)" }}>Up next</div>
          <div className="flex flex-wrap gap-1">
            {next_topics.map((t, i) => (
              <span key={i} className="text-10 px-2 py-0.5 rounded-full" style={{ background: ACCENT + "1A", color: ACCENT }}>
                {t}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ─── WorkedExampleBlock ───────────────────────────────── */
export function WorkedExampleBlock({ topic, problem, steps, answer }) {
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b flex items-center gap-2"
        style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <Target size={14} style={{ color: ACCENT }} />
        <span className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.55)" }}>Worked example · {topic}</span>
      </div>
      <div className="px-4 py-3">
        <div className="rounded-md p-3 mb-3" style={{ background: "rgba(255,255,255,0.04)" }}>
          <div className="text-9 uppercase tracking-tightest2 mb-1" style={{ color: "rgba(255,255,255,0.45)" }}>Problem</div>
          <div className="text-xs leading-relaxed" style={{ color: "rgba(255,255,255,0.9)" }}>{problem}</div>
        </div>

        <div className="mb-3">
          <div className="text-9 uppercase tracking-tightest2 mb-1.5" style={{ color: "rgba(255,255,255,0.45)" }}>Solution steps</div>
          <div className="space-y-1.5">
            {steps.map((s, i) => (
              <div key={i} className="flex items-start gap-2">
                <span className="text-10 font-mono font-medium flex-shrink-0 rounded-full flex items-center justify-center"
                  style={{ width: 18, height: 18, background: ACCENT + "22", color: ACCENT, marginTop: 1 }}>
                  {i + 1}
                </span>
                <span className="text-11 leading-relaxed font-mono" style={{ color: "rgba(255,255,255,0.85)", whiteSpace: "pre-wrap" }}>{s}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-md p-3 flex items-start gap-2"
          style={{ background: "rgba(134,239,172,0.08)", border: "1px solid rgba(134,239,172,0.2)" }}>
          <CheckCircle2 size={14} style={{ color: "#86efac", marginTop: 1, flexShrink: 0 }} />
          <div>
            <div className="text-9 uppercase tracking-tightest2 mb-0.5" style={{ color: "#86efac" }}>Answer</div>
            <div className="text-xs" style={{ color: "rgba(255,255,255,0.9)" }}>{answer}</div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ─── StudyPlanBlock ───────────────────────────────────── */
export function StudyPlanBlock({ title, horizon, sessions }) {
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b flex items-center justify-between"
        style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <div className="flex items-center gap-2">
          <Layers size={14} style={{ color: ACCENT }} />
          <span className="text-xs font-medium" style={{ color: "white" }}>{title}</span>
        </div>
        <span className="text-10 px-1.5 py-0.5 rounded-full" style={{ background: ACCENT + "1A", color: ACCENT }}>{horizon}</span>
      </div>
      <div className="px-4 py-3 space-y-3">
        {sessions.map((sess, i) => (
          <div key={i}>
            <div className="flex items-center gap-2 mb-1.5">
              <div className="text-10 font-mono font-medium px-2 py-0.5 rounded-full"
                style={{ background: ACCENT + "22", color: ACCENT }}>{sess.day}</div>
              <div className="flex-1 h-px" style={{ background: "rgba(255,255,255,0.08)" }} />
            </div>
            <div className="space-y-1 ml-2">
              {sess.blocks.map((b, j) => (
                <div key={j} className="flex items-start gap-2 px-2.5 py-2 rounded-md"
                  style={{ background: "rgba(255,255,255,0.02)" }}>
                  <Clock size={11} style={{ color: ACCENT, marginTop: 2, flexShrink: 0 }} />
                  <div className="flex-1 min-w-0">
                    <div className="text-xs" style={{ color: "rgba(255,255,255,0.9)" }}>
                      <span className="font-medium" style={{ color: "white" }}>{b.subject}</span>
                      <span style={{ color: "rgba(255,255,255,0.3)", margin: "0 4px" }}>·</span>
                      <span>{b.topic}</span>
                    </div>
                    <div className="text-10 mt-0.5" style={{ color: "rgba(255,255,255,0.55)" }}>
                      <span className="font-mono">{b.duration_min} min</span>
                      <span style={{ color: "rgba(255,255,255,0.3)", margin: "0 4px" }}>·</span>
                      <span style={{ color: ACCENT }}>{b.technique}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── StudyTechniquesBlock ─────────────────────────────── */
export function StudyTechniquesBlock({ title, items }) {
  return (
    <div className="space-y-2">
      {title && (
        <div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>
      )}
      {items.map((t) => (
        <div key={t.id} className="rounded-xl p-3 border"
          style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
          <div className="flex items-start gap-3">
            <div className="rounded-lg flex items-center justify-center flex-shrink-0"
              style={{ width: 36, height: 36, background: ACCENT + "14" }}>
              <Sparkles size={15} style={{ color: ACCENT }} />
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-sm font-medium mb-1" style={{ color: "white" }}>{t.name}</div>
              <div className="text-11 leading-relaxed mb-1.5" style={{ color: "rgba(255,255,255,0.7)" }}>{t.description}</div>
              <div className="text-10" style={{ color: "rgba(255,255,255,0.45)" }}>
                <span className="uppercase tracking-tightest2">Best for:</span>{" "}
                <span style={{ color: ACCENT }}>{t.best_for}</span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

/* ─── FlashcardsBlock — interactive flip ───────────────── */
export function FlashcardsBlock({ topic, cards }) {
  const [i, setI] = useState(0);
  const [flipped, setFlipped] = useState(false);

  const next = () => { setFlipped(false); setI((i + 1) % cards.length); };
  const prev = () => { setFlipped(false); setI((i - 1 + cards.length) % cards.length); };
  const card = cards[i];

  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b flex items-center justify-between"
        style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <div className="flex items-center gap-2">
          <BookMarked size={14} style={{ color: ACCENT }} />
          <span className="text-xs font-medium" style={{ color: "white" }}>{topic}</span>
        </div>
        <span className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>
          {i + 1} / {cards.length}
        </span>
      </div>
      <div className="p-4">
        <div className={`flashcard ${flipped ? "flipped" : ""}`}
          style={{ height: 140, cursor: "pointer" }}
          onClick={() => setFlipped(!flipped)}>
          <div className="flashcard-inner">
            <div className="flashcard-front rounded-lg"
              style={{ background: "rgba(255,255,255,0.04)", border: `1px solid ${ACCENT}33` }}>
              <div className="text-center">
                <div className="text-9 uppercase tracking-tightest2 mb-2" style={{ color: ACCENT }}>Question</div>
                <div className="text-sm" style={{ color: "rgba(255,255,255,0.92)" }}>{card.front}</div>
                <div className="text-10 mt-3" style={{ color: "rgba(255,255,255,0.4)" }}>Click to flip</div>
              </div>
            </div>
            <div className="flashcard-back rounded-lg"
              style={{ background: ACCENT + "1A", border: `1px solid ${ACCENT}55` }}>
              <div className="text-center">
                <div className="text-9 uppercase tracking-tightest2 mb-2" style={{ color: ACCENT }}>Answer</div>
                <div className="text-xs font-mono leading-relaxed" style={{ color: "white" }}>{card.back}</div>
              </div>
            </div>
          </div>
        </div>
        <div className="flex items-center justify-between mt-3">
          <button onClick={prev} className="text-xs px-3 py-1.5 rounded-md border"
            style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)", color: "rgba(255,255,255,0.7)" }}>
            ← Previous
          </button>
          <div className="flex items-center gap-1">
            {cards.map((_, idx) => (
              <div key={idx} className="rounded-full"
                style={{ width: 5, height: 5, background: idx === i ? ACCENT : "rgba(255,255,255,0.15)" }} />
            ))}
          </div>
          <button onClick={next} className="text-xs px-3 py-1.5 rounded-md border"
            style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)", color: "rgba(255,255,255,0.7)" }}>
            Next →
          </button>
        </div>
      </div>
    </div>
  );
}

/* ─── Dispatcher ───────────────────────────────────────── */
export default function Block({ block }) {
  switch (block.type) {
    case "text":             return <TextBlock {...block} />;
    case "disclaimer":       return <DisclaimerBlock {...block} />;
    case "integrity_alert":  return <IntegrityAlertBlock {...block} />;
    case "profile":          return <ProfileBlock {...block} />;
    case "courses":          return <CoursesBlock {...block} />;
    case "assignments":      return <AssignmentsBlock {...block} />;
    case "grades":           return <GradesBlock {...block} />;
    case "attendance":       return <AttendanceBlock {...block} />;
    case "schedule":         return <ScheduleBlock {...block} />;
    case "fees":             return <FeesBlock {...block} />;
    case "concept":          return <ConceptBlock {...block} />;
    case "worked_example":   return <WorkedExampleBlock {...block} />;
    case "study_plan":       return <StudyPlanBlock {...block} />;
    case "study_techniques": return <StudyTechniquesBlock {...block} />;
    case "flashcards":       return <FlashcardsBlock {...block} />;
    default:
      return (
        <div className="text-xs px-3 py-2 rounded-md" style={{ background: "rgba(255,255,255,0.04)", color: "rgba(255,255,255,0.5)" }}>
          [Unknown block type: {block.type}]
        </div>
      );
  }
}
