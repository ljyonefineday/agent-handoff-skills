from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAMES = ("handoff-init", "handoff-create", "handoff-resume")
LIMITS = {"handoff-init": 600, "handoff-create": 700, "handoff-resume": 550}
REFERENCES = {
    "handoff-init": "references/recovery.md",
    "handoff-create": "references/emergency.md",
    "handoff-resume": "references/conflicts.md",
}
CONFIG = """```yaml
version: 2
active_file: HANDOFF.md
history_directory: .handoff/history
validation_commands: []
checkpoint_policy: preserve-worktree
```"""
TEMPLATE = """```markdown
# Agent Handoff

## Metadata
## Objective
## Work State
### Completed
### In Progress
### Remaining
## Repository State
## Continuation Context
## Validation and Risks
## Next Action
```"""
LEGACY = (
    "version: 1",
    "## Completion Criteria",
    "## Current Status",
    "### Partially Completed",
    "### Not Started",
    "## Implemented Changes",
    "## Decisions and Rationale",
    "## Constraints and Invariants",
    "## Validation Results",
    "## Known Issues",
    "## Unverified Hypotheses",
    "## Next Recommended Action",
    "## Handoff Intake",
)
WORD_RE = re.compile(r"[^\W_]+(?:[-'’][^\W_]+)*|\d+", re.UNICODE)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def skill(name: str) -> str:
    return read(SKILLS / name / "SKILL.md")


def split_skill(name: str) -> tuple[dict[str, str], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", skill(name), re.DOTALL)
    if not match:
        raise AssertionError(f"{name}/SKILL.md needs one frontmatter block")
    metadata = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            metadata[key.strip()] = value.strip().strip('"')
    return metadata, match.group(2)


def words(text: str) -> int:
    return len(WORD_RE.findall(text))


class SkillStructureTests(unittest.TestCase):
    def test_names_and_frontmatter_are_stable(self) -> None:
        self.assertEqual(
            sorted(path.name for path in SKILLS.iterdir() if path.is_dir()),
            sorted(NAMES),
        )
        for name in NAMES:
            with self.subTest(skill=name):
                metadata, body = split_skill(name)
                self.assertEqual(set(metadata), {"name", "description"})
                self.assertEqual(metadata["name"], name)
                self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertTrue(body.strip())

    def test_descriptions_are_trigger_focused_and_agent_neutral(self) -> None:
        trigger_terms = {
            "handoff-init": ("repository", "setup"),
            "handoff-create": ("incomplete", "transfer"),
            "handoff-resume": ("continuing", "handoff"),
        }
        for name in NAMES:
            with self.subTest(skill=name):
                description = split_skill(name)[0]["description"]
                self.assertTrue(description.startswith("Use when "))
                self.assertLessEqual(words(description), 45)
                self.assertNotRegex(description, r"/handoff|Claude|Codex|OpenAI|ChatGPT")
                for term in trigger_terms[name]:
                    self.assertIn(term, description.lower())

    def test_runtime_bundle_is_markdown_only(self) -> None:
        files = [path for path in SKILLS.rglob("*") if path.is_file()]
        self.assertTrue(files)
        self.assertTrue(all(path.suffix == ".md" for path in files))
        self.assertFalse(any(path.name == "openai.yaml" for path in files))
        self.assertFalse(any("scripts" in path.parts or "agents" in path.parts for path in files))

    def test_direct_conditional_references_are_owned_and_resolve(self) -> None:
        link_re = re.compile(r"\[[^]]+\]\(([^)#?]+\.md)(?:#[^)]*)?\)")
        for name, expected in REFERENCES.items():
            with self.subTest(skill=name):
                directory = SKILLS / name
                body = split_skill(name)[1]
                self.assertEqual(link_re.findall(body), [expected])
                self.assertRegex(
                    body,
                    rf"(?is)(only when[^\n]*\[[^]]+\]\({re.escape(expected)}\)|"
                    rf"\[[^]]+\]\({re.escape(expected)}\)[^\n]*only when)",
                )
                target = (directory / expected).resolve()
                self.assertTrue(target.is_relative_to(directory.resolve()))
                self.assertTrue(target.is_file())
                self.assertEqual(Path(expected).parts[0], "references")
                self.assertEqual(len(Path(expected).parts), 2)

                for markdown in directory.rglob("*.md"):
                    for link in link_re.findall(read(markdown)):
                        self.assertNotIn("..", Path(link).parts)
                        linked = (markdown.parent / link).resolve()
                        self.assertTrue(linked.is_relative_to(directory.resolve()))
                        self.assertTrue(linked.is_file())

    def test_core_body_word_budgets(self) -> None:
        for name, limit in LIMITS.items():
            with self.subTest(skill=name):
                count = words(split_skill(name)[1])
                self.assertLessEqual(count, limit, f"{name} has {count} body words")


class ProtocolContractTests(unittest.TestCase):
    def test_exact_v2_config_and_template_replace_v1(self) -> None:
        init = skill("handoff-init")
        self.assertIn(CONFIG, init)
        self.assertIn(TEMPLATE, init)
        runtime = "\n".join(read(path) for path in SKILLS.rglob("*.md"))
        for legacy in LEGACY:
            with self.subTest(legacy=legacy):
                self.assertNotIn(legacy, runtime)

    def test_paths_are_repository_relative_and_non_escaping(self) -> None:
        for name in NAMES:
            with self.subTest(skill=name):
                body = split_skill(name)[1]
                self.assertIn("repository-relative", body)
                self.assertRegex(body, r"(?i)(absolute|path traversal|\.\.)")
                self.assertRegex(
                    body,
                    r"(?i)(resolve|remain|stay).{0,35}(within|inside).{0,35}repository root",
                )

    def test_preserve_worktree_rule_is_in_every_core(self) -> None:
        for name in NAMES:
            with self.subTest(skill=name):
                body = split_skill(name)[1].lower()
                self.assertIn("preserve-worktree", body)
                for operation in ("reset", "clean", "stash", "switch", "discard"):
                    self.assertIn(operation, body)

    def test_non_v2_is_incompatible_and_never_interpreted(self) -> None:
        for name in ("handoff-create", "handoff-resume"):
            with self.subTest(skill=name):
                body = split_skill(name)[1]
                self.assertRegex(body, r"(?i)do not interpret.{0,50}(v1|non-v2)")
                self.assertRegex(body, r"(?i)(missing|non-v2).{0,100}reference")

    def test_recovery_archives_before_write_or_changes_nothing(self) -> None:
        path = SKILLS / "handoff-init" / "references" / "recovery.md"
        self.assertTrue(path.is_file())
        text = read(path)
        self.assertIn(".handoff/history/protocol-backup-", text)
        self.assertRegex(text, r"(?i)incompatible|partial|damaged")
        self.assertRegex(text, r"(?i)unique")
        self.assertRegex(text, r"(?i)archiv.{0,100}(all|every).{0,60}(old|detected|existing)")
        self.assertRegex(text, r"(?i)archiv.{0,100}before.{0,100}(write|install)")
        self.assertRegex(text, r"(?i)archiv.{0,100}fail.{0,100}(unchanged|no changes)")
        self.assertRegex(text, r"(?i)unsafe.{0,30}path")

    def test_new_and_repaired_init_keep_validation_commands_empty(self) -> None:
        init = skill("handoff-init")
        recovery = read(SKILLS / "handoff-init" / "references" / "recovery.md")
        self.assertIn(
            "New and repaired setup must write `validation_commands: []` unchanged.",
            init,
        )
        self.assertRegex(init, r"(?i)do not (discover|add).{0,50}validation commands")
        self.assertRegex(
            recovery,
            r"(?is)unknown validation command.{0,160}(do not|never).{0,40}carry",
        )

    def test_archival_fails_closed_for_secret_bearing_artifacts(self) -> None:
        references = (
            SKILLS / "handoff-init" / "references" / "recovery.md",
            SKILLS / "handoff-create" / "references" / "emergency.md",
        )
        for path in references:
            with self.subTest(reference=path.relative_to(ROOT)):
                text = read(path)
                self.assertRegex(
                    text,
                    r"(?is)(known|suspected).{0,60}secret value.{0,160}(stop|abort)",
                )
                self.assertRegex(
                    text,
                    r"(?is)secret value.{0,220}(unchanged|no changes)",
                )
                self.assertRegex(text, r"(?i)saniti[sz]|rotat")


class CreateContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.body = split_skill("handoff-create")[1]

    def test_v2_sections_and_adaptive_sizes_are_explicit(self) -> None:
        for heading in (
            "## Metadata", "## Objective", "## Work State", "### Completed",
            "### In Progress", "### Remaining", "## Repository State",
            "## Continuation Context", "## Validation and Risks", "## Next Action",
        ):
            self.assertIn(heading, self.body)
        self.assertRegex(self.body, r"(?i)(simple.{0,30}450 words|450 words.{0,30}simple)")
        self.assertRegex(self.body, r"(?i)(complex.{0,30}900 words|900 words.{0,30}complex)")
        self.assertRegex(self.body, r"(?i)(soft target|not a hard cap)")
        self.assertRegex(self.body, r"(?i)(never omit|must not omit).{0,40}(critical|material)")
        self.assertNotRegex(self.body, r"(?i)target at most")

    def test_empty_unknown_and_continuation_context_contracts(self) -> None:
        self.assertIn("None material", self.body)
        self.assertIn("Unknown — reason", self.body)
        for term in ("decisions", "constraints", "rejected approaches", "environment", "services"):
            self.assertIn(term, self.body.lower())
        self.assertRegex(self.body, r"(?i)secret (names|paths).{0,50}never values")

    def test_validation_is_fresh_honest_and_separated(self) -> None:
        for result in ("PASS", "FAIL", "NOT RUN"):
            self.assertIn(result, self.body)
        for category in ("fresh evidence", "confirmed issues", "unverified hypotheses"):
            self.assertIn(category, self.body.lower())
        self.assertRegex(self.body, r"(?i)(stale|earlier).{0,50}PASS.{0,80}(fresh|current|re-run)")

    def test_next_action_is_exactly_one_and_executable(self) -> None:
        self.assertRegex(self.body, r"(?i)exactly one.{0,30}action")
        positions = []
        for field in (
            "Action:", "Target paths:", "First command:",
            "Expected current result:", "Completion condition:",
        ):
            self.assertIn(field, self.body)
            positions.append(self.body.index(field))
        self.assertEqual(positions, sorted(positions))

    def test_core_keeps_mutation_secret_and_epistemic_safety(self) -> None:
        self.assertRegex(self.body, r"(?i)only.{0,40}handoff artifacts")
        self.assertRegex(self.body, r"(?i)never.{0,30}secret.{0,30}values")
        self.assertRegex(self.body, r"(?i)(hypothes|unknown).{0,80}(evidence|verify|confirmed)")

    def test_core_stops_secret_bearing_archive(self) -> None:
        self.assertRegex(
            self.body,
            r"(?is)(known|suspected).{0,60}secret value.{0,120}stop",
        )
        self.assertRegex(
            self.body,
            r"(?is)secret value.{0,180}(unchanged|no changes)",
        )
        self.assertRegex(self.body, r"(?i)saniti[sz]|rotat")


class ResumeContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.body = split_skill("handoff-resume")[1]

    def test_live_state_is_ground_truth_and_inherited_work_is_safe(self) -> None:
        for command in (
            "git status --short", "git branch --show-current", "git log -5 --oneline",
            "git diff --stat", "git diff --cached --stat",
        ):
            self.assertIn(command, self.body)
        self.assertRegex(self.body, r"(?i)repository.{0,50}ground truth")
        self.assertRegex(self.body, r"(?i)preserve.{0,50}inherited")

    def test_acceptance_follows_verification(self) -> None:
        self.assertIn("ready → accepted", self.body)
        self.assertRegex(self.body, r"(?i)only after.{0,50}verif")
        self.assertIn("## Intake", self.body)
        self.assertRegex(self.body, r"(?i)append")

    def test_intake_is_a_compact_delta_with_one_gating_result(self) -> None:
        self.assertRegex(self.body, r"(?i)target.{0,30}200 words")
        self.assertRegex(self.body, r"(?i)not a hard cap|never omit")
        self.assertRegex(self.body, r"(?i)delta")
        self.assertRegex(self.body, r"(?i)do not duplicate.{0,40}(confirmed|handoff)")
        fields = (
            "Receiver:", "Timestamp:", "Verified state:", "Gating validation:",
            "Discrepancies:", "Next Action:",
        )
        positions = []
        for field in fields:
            self.assertIn(field, self.body)
            positions.append(self.body.index(field))
        self.assertEqual(positions, sorted(positions))
        self.assertRegex(self.body, r"(?i)exactly one fresh gating validation")
        self.assertRegex(self.body, r"(?i)(retain|replace).{0,40}Next Action")

    def test_stale_results_and_hypotheses_are_not_promoted(self) -> None:
        for result in ("PASS", "FAIL", "NOT RUN"):
            self.assertIn(result, self.body)
        self.assertRegex(self.body, r"(?i)stale.{0,50}PASS.{0,80}(fresh|current|re-run)")
        self.assertRegex(self.body, r"(?i)(unknown|hypothes).{0,80}(evidence|confirmed|verify)")


class ReadmeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(ROOT / "README.md")

    def test_introduction_is_portable_and_agent_neutral(self) -> None:
        introduction = cls_intro = self.text.split("##", 1)[0]
        self.assertRegex(introduction, r"(?i)portable Agent Skills")
        self.assertNotRegex(cls_intro, r"Three Claude Code skills")

    def test_managed_and_no_node_installation_cover_both_agents(self) -> None:
        self.assertIn("npx skills add", self.text)
        self.assertRegex(self.text, r"(?i)recommended")
        self.assertRegex(self.text, r"(?i)without Node|no-Node")
        for value in ("Claude Code", "~/.claude/skills", "Codex", "~/.agents/skills"):
            self.assertIn(value, self.text)

    def test_invocation_update_and_removal_are_documented(self) -> None:
        for invocation in (
            "/handoff-init", "/handoff-create", "/handoff-resume",
            "$handoff-init", "$handoff-create", "$handoff-resume",
        ):
            self.assertIn(invocation, self.text)
        self.assertIn("npx skills update", self.text)
        self.assertIn("npx skills remove", self.text)
        self.assertRegex(self.text, r"(?i)natural language")

    def test_v2_lifecycle_sizing_and_economics_are_explained(self) -> None:
        self.assertIn("version: 2", self.text)
        self.assertIn("ready → accepted", self.text)
        self.assertIn("## Intake", self.text)
        for size in ("450", "900", "200"):
            self.assertIn(size, self.text)
        self.assertRegex(self.text, r"(?i)(not economical|skip a handoff|not worth)")
        self.assertNotRegex(self.text, r"(?i)target: at most")


class EvaluationFixtureTests(unittest.TestCase):
    def test_five_fresh_context_scenarios_exist(self) -> None:
        fixture_dir = ROOT / "tests" / "fixtures"
        expected = {
            "high-context-dirty-work.md",
            "small-reconstructible-task.md",
            "stale-resume.md",
            "incompatible-init.md",
            "end-to-end-continuation.md",
        }
        self.assertEqual(
            {path.name for path in fixture_dir.glob("*.md") if path.name != "README.md"},
            expected,
        )

    def test_high_context_fixture_seeds_every_critical_fact(self) -> None:
        text = read(ROOT / "tests" / "fixtures" / "high-context-dirty-work.md")
        for term in (
            "User constraint", "Rejected approach", "Running service", "Secret path",
            "PASS", "FAIL", "NOT RUN",
        ):
            self.assertIn(term, text)
        self.assertRegex(text, r"(?i)never.{0,40}secret value")

    def test_small_fixture_requires_compactness(self) -> None:
        text = read(ROOT / "tests" / "fixtures" / "small-reconstructible-task.md")
        self.assertIn("450-word", text)
        self.assertIn("None material", text)
        self.assertRegex(text, r"(?i)compact")

    def test_stale_resume_seeds_all_drift(self) -> None:
        text = read(ROOT / "tests" / "fixtures" / "stale-resume.md")
        for term in ("branch drift", "HEAD drift", "extra changes", "stale PASS", "obsolete"):
            self.assertIn(term, text)

    def test_incompatible_init_preserves_user_material(self) -> None:
        text = read(ROOT / "tests" / "fixtures" / "incompatible-init.md")
        for term in ("partial", "version: 1", "user history", "unknown validation command"):
            self.assertIn(term, text)
        self.assertRegex(
            text,
            r"(?i)(leave.{0,50}unchanged.{0,80}archiv|archiv.{0,80}leave.{0,50}unchanged)",
        )
        self.assertIn("Secret-bearing variant", text)
        self.assertRegex(text, r"(?i)owner.{0,50}(reports|flags).{0,50}secret value")
        self.assertRegex(text, r"(?i)(stop|abort).{0,80}archiv.{0,100}unchanged")

    def test_end_to_end_receiver_has_only_repo_and_artifact(self) -> None:
        text = read(ROOT / "tests" / "fixtures" / "end-to-end-continuation.md")
        self.assertRegex(text, r"(?i)only the repository and.{0,30}(artifact|handoff)")
        for term in ("User constraint", "Rejected decision", "freshly FAIL", "Safe next action"):
            self.assertIn(term, text)

    def test_rubric_has_weights_fatal_errors_and_reduction_gate(self) -> None:
        text = read(ROOT / "tests" / "fixtures" / "README.md")
        weights = {
            "Continuity fidelity": "30%",
            "Repository and secret safety": "20%",
            "Validation honesty": "15%",
            "Next-action executability": "15%",
            "Resume correctness": "10%",
            "Token economy": "10%",
        }
        for category, weight in weights.items():
            self.assertRegex(text, rf"{re.escape(category)}[^\n]*{re.escape(weight)}")
        for variant in ("no-skill", "current", "revised"):
            self.assertIn(variant, text)
        self.assertIn("90/100", text)
        self.assertRegex(text, r"(?i)30%.{0,50}median.{0,60}create-plus-intake")
        for fatal in (
            "destructive mutation", "secret leak", "fabricated current result",
            "omitted seeded constraint", "omitted rejected decision", "unsafe next action",
        ):
            self.assertIn(fatal, text.lower())

    def test_evaluation_results_record_acceptance_evidence(self) -> None:
        path = ROOT / "tests" / "EVALUATION_RESULTS.md"
        self.assertTrue(path.is_file())
        text = read(path)
        for evidence in ("e7c2063", "100/100", "zero fatal", "49.2%", "675", "343"):
            self.assertIn(evidence, text)


if __name__ == "__main__":
    unittest.main()
