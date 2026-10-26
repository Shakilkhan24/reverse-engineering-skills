# Mission: Build a Modular, Production-Grade Reverse Engineering Skill System for AI Agents

## 1. Your Role and Mission

Act as a senior software architect, reverse engineer, systems engineer, AI-agent workflow designer, DevOps engineer, security engineer, and technical researcher.

Your mission is to analyze the comprehensive reverse-engineering instruction I have provided and transform it into a **modular, reusable, intelligently coordinated skill system** that enables capable AI agents to reconstruct, reproduce, improve, and engineer sophisticated software applications.

Do not merely summarize, shorten, or reorganize the original instruction. Understand its underlying purpose, extract its engineering principles, identify its weaknesses, and redesign it into a system that agents can execute reliably.

Think of the result as an engineering operating system for AI agents: a set of specialized capabilities, a coordination mechanism, clear execution procedures, and measurable quality standards.

The objective is to make an AI agent capable of approaching complex software projects with the discipline of an experienced engineering team rather than relying on a few vague prompts and generating code based on assumptions.

## 2. Understand the Real Problem Before Solving It

The original instruction may contain valuable knowledge across numerous engineering disciplines. However, placing everything into one enormous prompt creates several problems:

- Important instructions may be forgotten, diluted, or overshadowed by later instructions.
- The agent may understand the general objective but neglect critical implementation details.
- Complex tasks may be executed in the wrong order or without necessary dependencies.
- The agent may generate plausible-looking implementations without verifying their actual behavior.
- Different engineering concerns may be handled inconsistently or duplicated across the project.
- The agent may focus on visible features while neglecting architecture, data integrity, security, testing, reliability, deployment, and maintainability.
- The agent may claim completion without sufficient evidence that the application works.
- Limited context, tool availability, execution time, or model capability may prevent the agent from completing the entire task effectively.

Your system must directly address these failure modes.

Do not assume that simply dividing a long prompt into multiple files solves the problem. The skills must have clear responsibilities, appropriate boundaries, effective coordination, and a practical execution strategy.

## 3. Analyze the Original Instruction in Depth

Before designing any skills, thoroughly examine the original reverse-engineering instruction.

Analyze it from multiple perspectives:

### A. Semantic and conceptual analysis
- What is the ultimate objective?
- What explicit requirements and implicit expectations does it contain?
- What engineering principles make it valuable?
- What problems is each major section intended to solve?
- Which requirements are essential, complementary, repetitive, ambiguous, or missing?

### B. Software engineering analysis
Examine its coverage of application architecture, frontend and backend behavior, APIs, databases, state management, integrations, business logic, infrastructure, and other relevant engineering disciplines.

Identify where the instruction encourages genuine reconstruction of system behavior versus superficial imitation.

### C. Reverse-engineering methodology
Determine how the agent should discover an existing system's behavior from available evidence, such as source code, documentation, screenshots, user flows, network traces, API specifications, database schemas, configuration files, and observed outputs.

Distinguish verified facts from reasonable inferences and unresolved unknowns.

### D. AI-agent reliability
Evaluate how the instruction handles context limitations, task decomposition, memory and state management, tool selection, execution order, intermediate checkpoints, recovery from errors, and verification.

### E. Production engineering
Assess whether it sufficiently addresses security, data integrity, automated testing, performance, scalability, accessibility, observability, deployment, rollback, maintainability, and operational readiness.

### F. Practical value
Determine which parts materially improve the final product and which parts create unnecessary complexity, excessive instructions, or diminishing returns.

Produce a requirements and coverage matrix connecting the original instruction to its intended outcomes, current weaknesses, and proposed improvements.

Do not begin creating skills until you have a sufficiently clear understanding of the source instruction and its engineering objectives.

If the original instruction cannot be found among the supplied materials or accessible project files, ask me to provide it rather than inventing its contents.

## 4. Design the Skill Architecture

Design a cohesive collection of specialized skills that work together as one system.

**Optimize for engineering coverage, clarity, reusability, and execution reliability—not for the number of skills created.**

Do not create an excessive number of tiny skills for individual technologies or trivial operations. Equally, do not combine so many unrelated responsibilities into one skill that it becomes another overwhelming instruction.

Each skill should represent a meaningful engineering capability or a closely related group of responsibilities.

Consider the following areas when developing the architecture. Treat them as a starting point, not a mandatory list; determine the final structure from the source analysis.

- **Orchestration and project planning:** Understand the objective, choose the relevant skills, establish dependencies, allocate work, manage context, and track progress.
- **Product reconnaissance and reverse engineering:** Investigate the reference application, discover its behavior, map its features, identify constraints, and maintain an evidence-based understanding of the system.
- **Requirements and system architecture:** Convert observations into explicit requirements, architecture decisions, component boundaries, interface contracts, and implementation plans.
- **Frontend and experience reconstruction:** Reproduce relevant interfaces, interactions, navigation, responsive behavior, accessibility, and visual consistency.
- **Backend and API engineering:** Reconstruct business logic, application services, API contracts, integrations, validation, authentication flows, and error handling.
- **Data architecture and persistence:** Handle database design, schemas, relationships, migrations, transactions, data integrity, caching, consistency, and data lifecycle management.
- **Security and reliability:** Address authorization, input validation, secrets, dependency risks, threat modeling, failure handling, and secure defaults.
- **Testing and engineering verification:** Validate requirements, behavior, integrations, regression risks, performance, and overall release readiness.
- **Infrastructure and delivery:** Handle environment configuration, containers, CI/CD, deployment, infrastructure automation, rollback, and release management.
- **Observability and operations:** Establish appropriate logging, metrics, traces, diagnostics, health checks, alerts, and operational feedback.
- **Performance and scalability:** Identify bottlenecks, establish performance expectations, measure actual behavior, and optimize where justified.
- **Documentation and maintainability:** Preserve architecture knowledge, setup instructions, design decisions, operational procedures, and future development guidance.

You may merge, divide, rename, or omit these areas when the evidence justifies doing so. Add any important missing capabilities.

For each skill, define its specific purpose, boundaries, activation conditions, required inputs, expected outputs, dependencies, and quality requirements.

## 5. Create an Effective Orchestration System

The system must include a central orchestration capability that determines how the other skills are used.

It should:

1. Understand the user's goal, constraints, available reference materials, and expected outcome.
2. Assess the project type, complexity, uncertainty, and risk.
3. Select the relevant skills instead of invoking every skill for every project.
4. Determine execution order and dependencies.
5. Identify work that can proceed in parallel and work that requires earlier results.
6. Delegate focused tasks with clear inputs, expected outputs, and acceptance criteria.
7. Maintain a shared record of requirements, architectural decisions, assumptions, discoveries, unresolved questions, test results, and current progress.
8. Reconcile conflicting recommendations or implementation changes from different skills.
9. Verify that outputs from one skill satisfy the requirements of the next.
10. Detect failures, revisit incorrect assumptions, and trigger additional investigation or testing when necessary.
11. Summarize what has been completed, what remains incomplete, and what evidence supports the current status.

Do not assume that every AI platform supports autonomous agents, parallel execution, persistent memory, or cross-skill invocation. Discover the target environment's actual capabilities and design accordingly.

Where automatic coordination is unavailable, provide a practical sequential workflow that a single agent can execute.

## 6. Define a Consistent Contract for Every Skill

Every skill must follow a consistent, concise, and operationally useful structure.

Include the following elements where applicable:

**Identity and purpose**
- Name and concise description.
- The engineering problem it solves.
- When to invoke it and when not to invoke it.

**Inputs and outputs**
- Required context, artifacts, evidence, and dependencies.
- Expected deliverables and their format.
- Information that must be passed to downstream skills.

**Execution procedure**
- A clear, ordered workflow.
- Appropriate tool usage and research procedures.
- Decision points, dependencies, and conditions for further investigation.
- Relevant alternatives when the preferred approach is unsuitable.

**Quality and verification**
- Acceptance criteria for the work.
- How the agent must test or verify its results.
- Required evidence before reporting completion.
- Common failure modes and recovery procedures.

**Coordination**
- Which skills may need to run before or after this skill.
- What should be escalated to the orchestrator.
- How to record assumptions, unresolved issues, and significant decisions.

Keep each skill focused enough to be reusable without losing the engineering depth necessary to produce meaningful results.

Do not duplicate entire workflows across skills. Shared principles should be defined centrally and referenced consistently.

## 7. Establish a Disciplined Reverse-Engineering Workflow

The skills should collectively support an evidence-driven lifecycle rather than immediately jumping into implementation.

Design the workflow around the following stages, adapting them to the project:

### Stage 1: Discovery
Identify the target system, available artifacts, observable behavior, user requirements, technical constraints, and authorization boundaries.

### Stage 2: Reconstruction
Map the features, user journeys, system components, data flows, external dependencies, business rules, interfaces, and important edge cases.

### Stage 3: Specification
Convert findings into a structured requirements set. Record what is verified, what is inferred, what is unknown, and what requires clarification.

### Stage 4: Architecture and planning
Establish the system architecture, technology choices, interfaces, data model, security requirements, implementation order, and acceptance criteria.

### Stage 5: Incremental implementation
Build the application in coherent, testable increments. Establish a working foundation before expanding functionality, and integrate components continuously.

### Stage 6: Verification and refinement
Compare actual behavior against the requirements and reference system. Investigate discrepancies, fix defects, and repeat verification until the relevant acceptance criteria are satisfied or explicitly blocked.

### Stage 7: Production preparation
Evaluate security, data integrity, testing coverage, performance, accessibility, observability, deployment, configuration, recovery, documentation, and operational readiness.

### Stage 8: Delivery and handoff
Provide the implementation, setup instructions, architectural documentation, verification results, known limitations, and a clear list of remaining work.

The workflow must allow feedback between stages. New evidence discovered during implementation or testing may require changes to the requirements or architecture.

Do not treat the stages as a rigid waterfall process when iteration would produce a better result.

## 8. Enforce High Engineering Standards

The system should encourage production-quality engineering rather than merely generating a large quantity of code.

### Correctness
Every significant feature should be connected to explicit requirements and appropriate verification.

### Architectural integrity
Components should have coherent responsibilities, well-defined interfaces, manageable dependencies, and an architecture appropriate to the actual project.

### Data integrity
Data models, migrations, validation, transactions, persistence, concurrency, caching, and failure recovery should be considered whenever relevant.

### Security and privacy
Use secure defaults, appropriate access controls, safe handling of secrets, dependency review, and protection of sensitive data. Respect authorization, intellectual property, licensing, and applicable legal boundaries.

### Testing
Use a risk-appropriate combination of unit, integration, end-to-end, regression, security, performance, and other relevant tests. Do not confuse the existence of test files with successful verification.

### Reliability and maintainability
Include suitable error handling, configuration management, dependency management, logging, documentation, and recovery procedures.

### Delivery and operations
Make the application reproducible, configurable, testable, and deployable. Use CI/CD, infrastructure automation, monitoring, and rollback procedures where appropriate to the project.

### User experience
Treat visual fidelity, interaction behavior, accessibility, responsive design, and usability as real engineering requirements whenever the product involves a user interface.

Do not force every concern into every project. Scale the depth of investigation and implementation to the project's scope, risk, complexity, and intended deployment environment.

## 9. Prevent Hallucination and False Completion

Establish explicit rules that every skill must follow.

- Never invent reference-system behavior, API responses, database schemas, configuration values, test results, or successful deployments.
- Clearly distinguish observed facts, documented facts, assumptions, hypotheses, and unknowns.
- Investigate important uncertainties before making irreversible or high-impact decisions.
- Prefer direct evidence and reproducible tests over unsupported confidence.
- Never report a command, test, build, integration, or deployment as successful unless the available evidence supports that claim.
- If access to the reference application or a required tool is unavailable, explain the limitation and identify the best available alternative.
- If a task cannot be completed, report the blocker, its consequences, and the next practical step.
- Never sacrifice critical requirements silently to make the project appear complete.

The system should remain useful even when an individual skill or the underlying AI model performs imperfectly.

Prioritize high-impact requirements, preserve critical knowledge, validate intermediate outputs, and make incomplete work visible.

## 10. Research and Improve Beyond the Original Prompt

Do not limit your thinking to the contents of the supplied instruction.

Research additional methodologies, engineering practices, agent-design patterns, and established tools when they can materially improve the result.

Use research selectively and purposefully. Prioritize authoritative technical documentation, established engineering references, relevant open-source implementations, and credible practical evidence.

When researching platform-specific skill conventions, inspect the actual target environment and follow its documented format. When evaluating tools or frameworks, consider their capabilities, limitations, compatibility, maintenance, and practical usefulness.

Cite external sources in the accompanying analysis when research informs important recommendations.

Do not add fashionable technologies, unnecessary abstractions, or elaborate processes merely to make the system appear sophisticated. Every significant addition should solve a defined problem.

## 11. Design for Graceful Partial Execution

The skill system must remain useful under realistic constraints, including limited model capability, context windows, execution time, tool access, and available resources.

Design it so that an agent can still produce meaningful progress when it cannot execute the entire workflow.

Prioritize work according to:

- Impact on core functionality.
- Importance to correctness and security.
- Dependencies and architectural consequences.
- Risk of irreversible mistakes.
- Cost of postponing the work.
- Availability of evidence and verification methods.

Separate essential requirements from optional improvements.

If the agent can only complete a subset of the work, it should prioritize the foundations that make the greatest contribution to a coherent, working product. It must also clearly disclose omitted requirements and unverified areas.

The goal is to maximize useful engineering outcomes under imperfect execution—not to pretend that partial execution guarantees a production-ready application.

## 12. Deliverables

After analyzing the source instruction and designing the architecture, create the actual skill system in the target environment wherever tools and permissions allow.

Deliver the following:

**A. Reverse-engineering analysis**
- A structured explanation of the original instruction's strengths, weaknesses, implicit requirements, and engineering coverage.
- A requirements and coverage matrix.
- A prioritized list of missing capabilities and improvements.

**B. Skill architecture**
- A clear overview of the skill system.
- A central orchestration skill or equivalent coordination mechanism.
- A concise index describing every skill, its purpose, and its activation conditions.
- A dependency map and execution workflow.
- An explanation of how the skills exchange context and avoid duplication.

**C. Individual skill implementations**
- Complete, usable skill files in the format supported by the target platform.
- Clear instructions, inputs, outputs, workflows, quality gates, verification procedures, and handoff rules.
- Cross-references that allow the orchestrator to select and coordinate the appropriate skills.

**D. Usage documentation**
- Installation or integration instructions.
- A practical guide explaining how to use the system for a new project.
- Example workflows for different project types.
- Guidance on how to extend or modify the skill library without breaking its architecture.

**E. Validation and evaluation**
- A set of representative scenarios for testing the skill system.
- Checks for correct skill selection, dependency handling, requirement coverage, context preservation, and verification discipline.
- Examples of expected behavior when evidence is missing, a tool fails, or a task cannot be completed.
- Identified limitations and recommended improvements.

If the environment supports creating files, create the actual artifacts rather than returning only a conceptual proposal. If it supports an existing skills directory or established conventions, inspect and follow those conventions instead of inventing an incompatible structure.

Do not claim that files were created, skills were installed, or validation was completed unless those actions actually occurred.

## 13. Acceptance Criteria

The final system should satisfy these conditions:

1. It captures the essential intent and valuable engineering knowledge of the original instruction.
2. It improves coverage without blindly preserving unnecessary repetition.
3. It divides responsibilities into meaningful, reusable skills rather than an excessive collection of micro-instructions.
4. It coordinates the skills through explicit routing, dependencies, and shared project state.
5. It supports evidence-based reverse engineering and iterative implementation.
6. It addresses architecture, data, APIs, security, testing, deployment, operations, and other relevant engineering concerns.
7. It defines measurable quality gates and requires evidence for completion claims.
8. It can adapt to different application types, technology stacks, and levels of project complexity.
9. It remains practical when execution resources and AI capabilities are limited.
10. It can be maintained, extended, evaluated, and reused across future projects.

Evaluate the result against these criteria before declaring the work complete. Identify any unmet criteria explicitly.

## 14. How You Should Execute This Mission

Work methodically. Do not attempt to solve everything through one enormous generation step.

Proceed through distinct phases:

1. Locate and analyze the original instruction.
2. Establish the requirements, coverage matrix, and gaps.
3. Design and justify the skill architecture.
4. Create the orchestration mechanism and individual skills.
5. Validate their consistency, dependencies, and practical usability.
6. Test representative workflows and revise weaknesses.
7. Produce the final documentation and a clear implementation status report.

Maintain concise progress records and preserve important decisions between phases. Where the environment supports persistent project notes, use them to prevent context loss.

Avoid asking me questions that can be resolved through reasonable investigation. Ask for clarification only when a missing decision materially affects the architecture, scope, authorization, or correctness of the result.

You have the freedom to improve the original approach substantially, provided that your changes serve the underlying objective.

## Final Objective

Build a reusable engineering skill system that helps AI agents move beyond superficial code generation toward disciplined software reconstruction and development.

I want the agent to investigate before assuming, plan before implementing, use specialized capabilities when appropriate, verify before claiming success, and deliver maintainable software with a clear understanding of its limitations.

The ultimate measure of success is not the length of the prompts, the number of skills, or the sophistication of the documentation.

**It is whether the system consistently helps an AI agent produce more correct, complete, secure, maintainable, testable, and deployable software than it would produce from a generic, all-in-one instruction.**

Think deeply, research where useful, engineer pragmatically, validate your work, and deliver the actual usable system.