import { Check, Clock, HandHelping, ServerCog, X } from 'lucide-react'
import type { ApprovalItem as ApprovalItemModel } from '../../types'
import { formatRelativeTime } from '../../lib/formatters'
import Badge, { severityTone } from '../ui/Badge'
import ExecutionPath from './ExecutionPath'

interface ApprovalItemProps {
  item: ApprovalItemModel
  /** Resolved display name for the workload (falls back to the id). */
  workloadName: string
  /** True while an action on this item is in flight (disables buttons). */
  busy?: boolean
  /** Open the approve confirmation (with optional MCP tool selection). */
  onApprove: () => void
  /** Open the manual-intervention confirmation. */
  onIntervene: () => void
  /** Open the deny confirmation. */
  onDeny: () => void
}

/** Humanize a snake_case enum into a readable label. */
function humanize(value: string): string {
  return value
    .split('_')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ')
}

const ACTION_BTN =
  'inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-50'

/**
 * A single approval-queue card: workload, recommended action, AI rationale,
 * risk/environment/MCP-tool context, time-since-request, and
 * Approve / Manual Intervention / Deny actions (design.md §Approval Queue).
 */
export default function ApprovalItem({
  item,
  workloadName,
  busy = false,
  onApprove,
  onIntervene,
  onDeny,
}: ApprovalItemProps) {
  const isCritical = item.severity === 'critical'
  const canDecide = item.status === 'pending' || item.status === 'snoozed'
  const path = item.status === 'escalated' ? 'escalation' : 'approval'

  return (
    <article
      className={[
        'card p-5',
        isCritical ? 'ring-1 ring-inset ring-critical-500/40' : '',
      ]
        .filter(Boolean)
        .join(' ')}
    >
      {/* Header: workload + severity + execution path */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          {isCritical && (
            <span
              className="h-2.5 w-2.5 shrink-0 animate-pulseRing rounded-full bg-critical-500"
              aria-hidden
            />
          )}
          <div>
            <p className="eyebrow">Workload</p>
            <h3 className="text-base font-semibold text-navy-50">{workloadName}</h3>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Badge tone={severityTone(item.severity)} uppercase>
            {item.severity}
          </Badge>
          {/* Distinguish a human escalation from a routine approval. */}
          {item.execution_mode === 'human_escalation_required' ? (
            <Badge tone="critical" uppercase>
              Escalation
            </Badge>
          ) : (
            <Badge tone="neutral" uppercase>
              Approval
            </Badge>
          )}
          <ExecutionPath path={path} />
        </div>
      </div>

      {/* Recommended action */}
      <div className="mt-4">
        <p className="eyebrow">Recommended action</p>
        <p className="mt-1 text-sm font-medium text-navy-50">
          {item.recommended_action}
        </p>
      </div>

      {/* AI rationale */}
      {item.ai_rationale && (
        <div className="mt-3">
          <p className="eyebrow">AI rationale</p>
          <p className="mt-1 text-sm text-navy-200">{item.ai_rationale}</p>
        </div>
      )}

      {/* Context row: risk, environment, category */}
      <div className="mt-4 flex flex-wrap items-center gap-2 text-xs">
        <Badge tone={severityTone(item.risk_level)} uppercase>
          {item.risk_level} risk
        </Badge>
        {item.environment && <Badge>{humanize(item.environment)}</Badge>}
        <Badge>{humanize(item.action_category)}</Badge>
      </div>

      {/* MCP tools */}
      {item.mcp_tools.length > 0 && (
        <div className="mt-4">
          <p className="eyebrow flex items-center gap-1.5">
            <ServerCog className="h-3.5 w-3.5" aria-hidden />
            MCP tools
          </p>
          <div className="mt-1.5 flex flex-wrap gap-1.5">
            {item.mcp_tools.map((tool) => (
              <span
                key={tool}
                className="rounded-md bg-navy-900 px-2 py-1 font-mono text-xs text-navy-200 ring-1 ring-inset ring-navy-700"
              >
                {tool}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Footer: timing + actions */}
      <div className="mt-5 flex flex-wrap items-center justify-between gap-3 border-t border-navy-700 pt-4">
        <div className="flex flex-wrap items-center gap-4">
          <span className="inline-flex items-center gap-1.5 text-xs text-navy-300">
            <Clock className="h-3.5 w-3.5" aria-hidden />
            {formatRelativeTime(item.created_at)}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={onApprove}
            disabled={busy || !canDecide}
            className={`${ACTION_BTN} bg-healthy-500/15 text-healthy-700 hover:bg-healthy-500/25`}
          >
            <Check className="h-4 w-4" aria-hidden />
            Approve
          </button>
          <button
            type="button"
            onClick={onIntervene}
            disabled={busy || !canDecide}
            className={`${ACTION_BTN} bg-warning-500/15 text-warning-700 hover:bg-warning-500/25`}
          >
            <HandHelping className="h-4 w-4" aria-hidden />
            Manual Intervention
          </button>
          <button
            type="button"
            onClick={onDeny}
            disabled={busy || !canDecide}
            className={`${ACTION_BTN} bg-critical-500/15 text-critical-700 hover:bg-critical-500/25`}
          >
            <X className="h-4 w-4" aria-hidden />
            Deny
          </button>
        </div>
      </div>
    </article>
  )
}
