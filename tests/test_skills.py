import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
EXPECTED_SKILLS = {"handoff-init", "handoff-create", "handoff-resume"}
LEGACY_NAMES = {
    "initializing-agent-handoffs",
    "creating-agent-handoffs",
    "resuming-agent-handoffs",
}


def read_skill(name: str) -> str:
    path = SKILLS_ROOT / name / "SKILL.md"
    assert path.is_file(), f"missing expected skill: {path}"
    return path.read_text(encoding="utf-8")


def frontmatter_name(document: str) -> str:
    match = re.match(r"---\n(?P<header>.*?)\n---\n", document, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md is missing YAML frontmatter")
    name = re.search(r"^name:\s*(.+)$", match.group("header"), re.MULTILINE)
    if name is None:
        raise AssertionError("SKILL.md frontmatter is missing name")
    return name.group(1).strip()


class SkillContractTests(unittest.TestCase):
    def test_skill_directories_use_short_names(self) -> None:
        actual = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(actual, EXPECTED_SKILLS)

    def test_frontmatter_names_match_directories(self) -> None:
        for name in EXPECTED_SKILLS:
            with self.subTest(skill=name):
                self.assertEqual(frontmatter_name(read_skill(name)), name)

    def test_legacy_names_are_not_referenced(self) -> None:
        combined = "\n".join(read_skill(name) for name in EXPECTED_SKILLS)
        for legacy_name in LEGACY_NAMES:
            with self.subTest(name=legacy_name):
                self.assertNotIn(legacy_name, combined)

    def test_optional_agent_metadata_is_absent(self) -> None:
        for name in EXPECTED_SKILLS:
            with self.subTest(skill=name):
                self.assertFalse((SKILLS_ROOT / name / "agents").exists())

    def test_init_requires_exact_contract_repair(self) -> None:
        document = read_skill("handoff-init")
        self.assertIn("write the exact contract below", document)
        self.assertIn("Never invent substitute headings", document)

    def test_init_preserves_unknown_existing_commands(self) -> None:
        document = read_skill("handoff-init")
        self.assertIn("Preserve an existing unverified command", document)

    def test_create_has_a_strict_mutation_budget(self) -> None:
        document = read_skill("handoff-create")
        self.assertIn("Mutation Budget", document)
        self.assertIn("Leave implementation files and untracked files in place", document)
        self.assertIn("one action, not a checklist", document)

    def test_resume_defines_acceptance_semantics(self) -> None:
        document = read_skill("handoff-resume")
        self.assertIn("Acceptance Semantics", document)
        self.assertIn("does not endorse every handoff claim", document)
        self.assertIn("If no active handoff exists", document)


if __name__ == "__main__":
    unittest.main()
