from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import run_model_tool_loop
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"

load_lab_env(ROOT)


def safe_slug(value: str) -> str:
    return "_".join(value.strip().split())[:80] or "run"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def write_transcript(path: Path, transcript: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    st.set_page_config(page_title="AI Trend Detective", layout="wide")
    st.title("AI Trend Detective")
    st.markdown(
        "Agent nghiên cứu trend AI: thu thập evidence, đánh giá hype và đưa ra verdict." 
        "Dùng `lookup`, `social_search`, `timeline`, `papers`, `evidence_judge`, `format`."
    )

    with st.sidebar:
        provider_name = st.selectbox("Provider", ["openrouter", "openai", "anthropic", "gemini"], index=0)
        version = st.text_input("Artifact version", "v0")
        model_override = st.text_input("Model (optional)", "")
        max_tool_rounds = st.number_input("Max tool rounds", min_value=1, max_value=6, value=4)
        system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
        tools_path = ARTIFACTS_DIR / "tools.yaml"

        st.write("### Artifact files")
        st.write(f"- system_prompt: `{system_prompt_path.name}`")
        st.write(f"- tools: `{tools_path.name}`")

    tool_declarations = load_tool_declarations(tools_path)
    openai_tools = to_openai_tools(tool_declarations)

    system_prompt_text = system_prompt_path.read_text(encoding="utf-8")
    st.sidebar.write("### System prompt snapshot")
    st.sidebar.code(system_prompt_text[:500] + ("..." if len(system_prompt_text) > 500 else ""), language="markdown")

    query = st.text_area("Nhập yêu cầu của bạn", height=140)
    run_button = st.button("Chạy agent")

    if run_button and query.strip():
        provider = make_provider(provider_name)
        selected_model = model_override or getattr(provider, "default_model", None)
        messages = [{"role": "system", "content": system_prompt_text}, {"role": "user", "content": query.strip()}]

        with st.spinner("Đang chạy agent ..."):
            result = run_model_tool_loop(
                provider=provider,
                messages=messages,
                tools=openai_tools,
                model=selected_model,
                max_tool_rounds=int(max_tool_rounds),
            )

        st.success("Hoàn tất")
        st.write("## Kết quả tổng quan")
        st.write(f"- Version: `{version}`")
        st.write(f"- Provider: `{provider_name}`")
        st.write(f"- Model: `{selected_model}`")
        st.write(f"- Status: `{result['status']}`")

        st.write("## Phản hồi cuối")
        st.markdown(result["assistant_text"] or "(No response)")

        st.write("## Tool rounds")
        for round_record in result["rounds"]:
            st.write(f"### Round {round_record['round']}")
            st.write("**Assistant text:**")
            st.markdown(round_record["assistant_text"] or "(no text)")
            if round_record["tool_calls"]:
                st.write("**Tool calls:**")
                st.json(round_record["tool_calls"])
            if round_record["tool_results"]:
                st.write("**Tool results:**")
                st.json(round_record["tool_results"])

        transcript_id = f"{safe_slug(version)}_{safe_slug(provider_name)}_{datetime.now().strftime('%Y%m%dT%H%M%S')}"
        transcript_path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"
        transcript = {
            "transcript_id": transcript_id,
            "provider": provider_name,
            "model": selected_model,
            "version": version,
            "created_at": now_iso(),
            "query": query.strip(),
            "status": result["status"],
            "assistant_text": result["assistant_text"],
            "rounds": result["rounds"],
            "tool_events": result.get("tool_events", []),
        }
        write_transcript(transcript_path, transcript)
        st.write("## Transcript saved")
        st.code(str(transcript_path))

    if not run_button:
        st.info("Nhập một yêu cầu và nhấn 'Chạy agent' để bắt đầu.")


if __name__ == "__main__":
    main()
