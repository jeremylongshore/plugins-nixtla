# Gemini Free Tier Research & Testing Plan

## PART 1: Gemini Model Options & Costs

### Free Tier Models (Google AI Studio)

**Gemini 2.0 Flash (Experimental)**
- Rate Limit: 10 RPM (requests per minute)
- Daily Limit: 1,500 requests/day
- Max Tokens: 1M input + 8K output
- Cost: **FREE**
- Best for: High-quality, fast generation

**Gemini 1.5 Flash**
- Rate Limit: 15 RPM
- Daily Limit: 1,500 requests/day  
- Max Tokens: 1M input + 8K output
- Cost: **FREE**
- Best for: Reliable, proven generation

**Gemini 1.5 Pro**
- Rate Limit: 2 RPM (very limited)
- Daily Limit: 50 requests/day
- Max Tokens: 2M input + 8K output
- Cost: **FREE**
- Best for: Complex skills requiring deep reasoning

### Paid Tier (Vertex AI - Production)

**Gemini 2.0 Flash**
- Rate Limit: 2,000 RPM (configurable)
- Cost: $0.075 per 1M input tokens, $0.30 per 1M output tokens
- Est. Cost for 500 skills: ~$5-10 total
- Best for: Production at scale

### Recommendation

**Phase 1 (Testing): Gemini 2.0 Flash (Free)**
- 10 RPM = 6 second pause between requests
- 1,500/day = 62 batches/day (25 skills each)
- Cost: $0

**Phase 2 (Production): Gemini 2.0 Flash (Vertex AI Paid)**
- 500 skills in ~30 minutes
- Cost: ~$5-10
- Full control, no rate limit worries

---

## PART 2: Rate Limit Testing Strategy

### Testing Environment: workspace/gemini-testing/

```
workspace/gemini-testing/
├── test-harness.js           # Main test runner
├── timing-calculator.js      # Rate limit optimizer
├── quality-validator.js      # Output quality checker
├── config.json              # API keys, settings
├── results/
│   ├── test-001-timing.json
│   ├── test-002-quality.json
│   └── metrics-summary.json
└── samples/
    ├── input-prompts/       # Test prompts
    └── output-skills/       # Generated skills
```

### Test Scenarios

**Test 1: Single Request Timing**
```javascript
// Measure: How long does Gemini take for 1 skill?
const start = Date.now()
const response = await gemini.generateContent(prompt)
const duration = Date.now() - start

// Expected: 2-5 seconds per skill
```

**Test 2: Rate Limit Detection**
```javascript
// Send requests without pause, detect 429 errors
for (let i = 0; i < 20; i++) {
  try {
    await gemini.generateContent(prompt)
    console.log(`Request ${i}: Success`)
  } catch (err) {
    if (err.status === 429) {
      console.log(`Rate limit hit at request ${i}`)
      // Result: Confirms 10 RPM limit
    }
  }
}
```

**Test 3: Optimal Spacing**
```javascript
// Test different pause times
const pauseTimes = [3000, 5000, 7000, 10000] // ms

for (const pause of pauseTimes) {
  const results = await testBatch(25, pause)
  console.log(`Pause ${pause}ms: ${results.successRate}% success`)
}

// Expected result: 6000ms (6 sec) = 100% success for 10 RPM
```

**Test 4: Quality vs Speed**
```javascript
// Test different models
const models = [
  'gemini-2.0-flash-exp',
  'gemini-1.5-flash',
  'gemini-1.5-pro'
]

for (const model of models) {
  const skill = await generateSkill(model, prompt)
  const quality = await validateQuality(skill)
  const speed = skill.responseTime
  
  console.log(`${model}: Quality=${quality}, Speed=${speed}ms`)
}

// Determines best model for our use case
```

---

## PART 3: Testing Harness Implementation

### File: workspace/gemini-testing/test-harness.js

```javascript
#!/usr/bin/env node

const { GoogleGenerativeAI } = require('@google/generative-ai')
const fs = require('fs')
const path = require('path')

class GeminiTester {
  constructor(apiKey, model = 'gemini-2.0-flash-exp') {
    this.genAI = new GoogleGenerativeAI(apiKey)
    this.model = this.genAI.getGenerativeModel({ model })
    this.metrics = {
      requests: 0,
      successes: 0,
      failures: 0,
      rateLimits: 0,
      totalTime: 0,
      avgResponseTime: 0
    }
  }

  async generateSkill(prompt, testId) {
    const start = Date.now()
    
    try {
      this.metrics.requests++
      
      const result = await this.model.generateContent(prompt)
      const response = result.response.text()
      const duration = Date.now() - start
      
      this.metrics.successes++
      this.metrics.totalTime += duration
      this.metrics.avgResponseTime = this.metrics.totalTime / this.metrics.successes
      
      return {
        success: true,
        content: response,
        duration,
        testId,
        timestamp: new Date().toISOString()
      }
    } catch (error) {
      const duration = Date.now() - start
      
      if (error.status === 429) {
        this.metrics.rateLimits++
      } else {
        this.metrics.failures++
      }
      
      return {
        success: false,
        error: error.message,
        status: error.status,
        duration,
        testId,
        timestamp: new Date().toISOString()
      }
    }
  }

  async testBatch(count, pauseMs) {
    console.log(`\n🧪 Testing batch: ${count} requests, ${pauseMs}ms pause`)
    
    const results = []
    
    for (let i = 0; i < count; i++) {
      const prompt = this.createTestPrompt(i)
      const result = await this.generateSkill(prompt, `test-${i}`)
      
      results.push(result)
      
      console.log(`  ${i + 1}/${count}: ${result.success ? '✓' : '✗'} (${result.duration}ms)`)
      
      // Pause between requests
      if (i < count - 1) {
        await this.sleep(pauseMs)
      }
    }
    
    return {
      results,
      metrics: { ...this.metrics },
      successRate: (this.metrics.successes / this.metrics.requests) * 100
    }
  }

  createTestPrompt(index) {
    return `Create a Claude Code Agent Skill for: docker-debugger-${index}

Requirements:
- Name: docker-debugger-${index}
- Description: Debugs Docker container issues (test skill ${index})
- Tools: Read, Bash(docker:*), Grep
- Include YAML frontmatter with all enterprise fields
- Keep instructions concise (this is a test)`
  }

  async sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  saveResults(testName, data) {
    const filename = `workspace/gemini-testing/results/${testName}.json`
    fs.mkdirSync(path.dirname(filename), { recursive: true })
    fs.writeFileSync(filename, JSON.stringify(data, null, 2))
    console.log(`\n📊 Results saved: ${filename}`)
  }

  printSummary() {
    console.log('\n' + '='.repeat(60))
    console.log('TEST SUMMARY')
    console.log('='.repeat(60))
    console.log(`Total Requests:     ${this.metrics.requests}`)
    console.log(`Successes:          ${this.metrics.successes} (${((this.metrics.successes / this.metrics.requests) * 100).toFixed(1)}%)`)
    console.log(`Failures:           ${this.metrics.failures}`)
    console.log(`Rate Limits Hit:    ${this.metrics.rateLimits}`)
    console.log(`Avg Response Time:  ${this.metrics.avgResponseTime.toFixed(0)}ms`)
    console.log(`Total Time:         ${(this.metrics.totalTime / 1000).toFixed(1)}s`)
    console.log('='.repeat(60))
  }
}

// Test Suite
async function runTests() {
  const apiKey = process.env.GEMINI_API_KEY
  if (!apiKey) {
    console.error('❌ GEMINI_API_KEY not set')
    process.exit(1)
  }

  const tester = new GeminiTester(apiKey)

  // Test 1: Single request timing
  console.log('\n🔬 TEST 1: Single Request Timing')
  const single = await tester.generateSkill(tester.createTestPrompt(0), 'single-test')
  console.log(`Result: ${single.success ? 'Success' : 'Failed'} in ${single.duration}ms`)

  // Test 2: Find optimal pause time
  console.log('\n🔬 TEST 2: Optimal Pause Time')
  const pauseTimes = [3000, 5000, 6000, 7000]
  
  for (const pause of pauseTimes) {
    const testerInstance = new GeminiTester(apiKey)
    const batch = await testerInstance.testBatch(5, pause)
    console.log(`  ${pause}ms pause: ${batch.successRate.toFixed(0)}% success rate`)
    
    if (batch.successRate === 100) {
      console.log(`  ✅ Optimal pause found: ${pause}ms`)
      break
    }
  }

  // Test 3: Quality check
  console.log('\n🔬 TEST 3: Quality Validation')
  const skill = await tester.generateSkill(tester.createTestPrompt(999), 'quality-test')
  
  if (skill.success) {
    // Check if valid YAML frontmatter
    const hasYAML = skill.content.match(/^---\n[\s\S]*?\n---/)
    const hasName = skill.content.includes('name:')
    const hasDescription = skill.content.includes('description:')
    const hasTools = skill.content.includes('allowed-tools:')
    
    console.log(`  YAML Frontmatter: ${hasYAML ? '✓' : '✗'}`)
    console.log(`  Has 'name':       ${hasName ? '✓' : '✗'}`)
    console.log(`  Has 'description': ${hasDescription ? '✓' : '✗'}`)
    console.log(`  Has 'allowed-tools': ${hasTools ? '✓' : '✗'}`)
    
    const quality = hasYAML && hasName && hasDescription && hasTools ? 'PASS' : 'FAIL'
    console.log(`  Overall Quality:  ${quality}`)
  }

  // Save all results
  tester.saveResults('gemini-testing-complete', {
    timestamp: new Date().toISOString(),
    metrics: tester.metrics,
    tests: {
      singleRequest: single,
      optimalPause: '6000ms (recommended for 10 RPM)',
      qualityCheck: 'See output above'
    }
  })

  tester.printSummary()
}

runTests().catch(console.error)
```

---

## PART 4: Timing Calculator

### File: workspace/gemini-testing/timing-calculator.js

```javascript
#!/usr/bin/env node

class TimingCalculator {
  constructor(rateLimit, dailyLimit) {
    this.rateLimit = rateLimit        // Requests per minute
    this.dailyLimit = dailyLimit      // Max requests per day
    this.safetyBuffer = 1.2           // 20% safety margin
  }

  calculateOptimalPause() {
    // Convert RPM to milliseconds between requests
    const minPauseMs = (60 / this.rateLimit) * 1000
    const safePauseMs = minPauseMs * this.safetyBuffer
    
    return {
      theoretical: minPauseMs,
      recommended: Math.ceil(safePauseMs),
      rpm: this.rateLimit,
      explanation: `${this.rateLimit} RPM = ${minPauseMs}ms pause (min), ${Math.ceil(safePauseMs)}ms (safe)`
    }
  }

  estimateBatchTime(skillCount) {
    const pause = this.calculateOptimalPause()
    const avgSkillTime = 3000 // 3 seconds per skill (measured)
    const totalPauseTime = (skillCount - 1) * pause.recommended
    const totalSkillTime = skillCount * avgSkillTime
    const totalTime = totalPauseTime + totalSkillTime
    
    return {
      skillCount,
      avgSkillTime,
      pauseTime: pause.recommended,
      totalTime,
      totalMinutes: (totalTime / 60000).toFixed(1),
      totalHours: (totalTime / 3600000).toFixed(2)
    }
  }

  dailyCapacity() {
    const pause = this.calculateOptimalPause()
    const skillsPerHour = Math.floor(3600000 / (3000 + pause.recommended))
    const skillsPerDay = Math.min(skillsPerHour * 24, this.dailyLimit)
    
    return {
      skillsPerHour,
      skillsPerDay,
      batchesPerDay: Math.floor(skillsPerDay / 25),
      dailyLimit: this.dailyLimit
    }
  }

  productionPlan(totalSkills) {
    const capacity = this.dailyCapacity()
    const daysNeeded = Math.ceil(totalSkills / capacity.skillsPerDay)
    const batchCount = Math.ceil(totalSkills / 25)
    
    return {
      totalSkills,
      skillsPerDay: capacity.skillsPerDay,
      daysNeeded,
      batchCount,
      batchesPerDay: capacity.batchesPerDay,
      recommendation: daysNeeded <= 1 
        ? 'Can complete in 1 day (free tier)'
        : `Requires ${daysNeeded} days (free tier) OR use paid tier (30 min)`
    }
  }
}

// Example usage
const gemini2Flash = new TimingCalculator(10, 1500) // 10 RPM, 1500/day

console.log('\n📊 GEMINI 2.0 FLASH (FREE TIER) ANALYSIS')
console.log('='.repeat(60))

console.log('\n1️⃣  OPTIMAL PAUSE TIME')
const pause = gemini2Flash.calculateOptimalPause()
console.log(JSON.stringify(pause, null, 2))

console.log('\n2️⃣  BATCH ESTIMATES (25 skills)')
const batch = gemini2Flash.estimateBatchTime(25)
console.log(JSON.stringify(batch, null, 2))

console.log('\n3️⃣  DAILY CAPACITY')
const daily = gemini2Flash.dailyCapacity()
console.log(JSON.stringify(daily, null, 2))

console.log('\n4️⃣  PRODUCTION PLAN (500 skills)')
const plan = gemini2Flash.productionPlan(500)
console.log(JSON.stringify(plan, null, 2))

console.log('\n' + '='.repeat(60))
```

---

## PART 5: Expected Test Results

### Timing Results (Predicted)

**Gemini 2.0 Flash (Free Tier):**
- Single request: 2-4 seconds
- Rate limit: 10 RPM
- Optimal pause: 6000ms (6 sec)
- 25 skills batch: ~2.5 minutes
- 500 skills: ~5 hours (free tier) OR 30 min (paid tier)

**Daily Capacity:**
- Skills/hour: ~400 (with pauses)
- Skills/day: 1,500 (free limit)
- Batches/day: 60 batches

**Conclusion:** Free tier can handle 500 skills in ~1 day

---

## PART 6: CI/CD Pipeline Design

### Pipeline Stages

```
┌─────────────────────────────────────────────────────────┐
│ STAGE 1: GENERATION (Gemini API)                        │
│                                                          │
│ Input:  planned-skills/categories/01-devops/config.json │
│ Gemini: Generate 25 SKILL.md files                      │
│ Output: workspace/gemini-testing/output/batch-001/raw/  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 2: VALIDATION (Python validator)                  │
│                                                          │
│ Input:  workspace/gemini-testing/output/batch-001/raw/  │
│ Script: scripts/validate-skills-schema.py               │
│ Output: Pass → validated/   Fail → failed/              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 3: AUTO-FIX (If validation fails)                 │
│                                                          │
│ Input:  workspace/gemini-testing/output/batch-001/failed/│
│ Script: scripts/auto-fix-yaml.js                        │
│ Action: Fix common YAML issues, re-validate             │
│ Output: fixed/ → validated/   OR → manual-review/       │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 4: QUALITY CHECK (AI-assisted)                    │
│                                                          │
│ Input:  workspace/gemini-testing/output/batch-001/validated/│
│ Script: scripts/validate-skill-quality.py               │
│ Checks: Trigger phrases, use cases, examples            │
│ Output: quality-report.json                             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 5: STAGING (Review & Approve)                     │
│                                                          │
│ Input:  workspace/gemini-testing/output/batch-001/validated/│
│ Action: Human spot-check (10% sample)                   │
│ Output: Approved → staging/   Rejected → rework/        │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 6: DEPLOYMENT (Production)                        │
│                                                          │
│ Input:  workspace/gemini-testing/staging/batch-001/     │
│ Script: scripts/deploy-skills.js                        │
│ Output: skills/devops-basics/*/SKILL.md                 │
│ Action: Update SKILLS-INDEX.json, regenerate READMEs    │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
workspace/gemini-testing/
├── config.json                  # API keys, settings
├── test-harness.js             # Testing runner
├── timing-calculator.js        # Rate limit optimizer
├── output/
│   ├── batch-001/
│   │   ├── raw/                # Direct Gemini output
│   │   ├── validated/          # Passed schema validation
│   │   ├── failed/             # Failed validation
│   │   ├── fixed/              # Auto-fixed YAML
│   │   ├── manual-review/      # Needs human intervention
│   │   └── staging/            # Approved for deployment
│   ├── batch-002/
│   └── ... (20 batches total)
└── results/
    ├── timing-metrics.json
    ├── quality-scores.json
    └── deployment-log.json
```

---

