# AI-Powered Courier Service Marketplace

## AIM OF PROJECT

Develop a service that leverages well-entrenched interfaces such as calendar and WhatsApp alongside Fetch.ai technology, such as the agent framework and the Fetch platform, to create a double-sided marketplace of couriers powered by AI. This service will run a courier service marketplace where consumers can autonomously find couriers, and courier service providers can autonomously find consumers for whom they deliver packages based on their respective criteria.

## INTRODUCTION

Develop several Fetch AI agents (using Fetch’s Python agent framework) that will orchestrate an AI-powered courier marketplace.

### Calendar & WhatsApp

Consumers and Courier Service Providers will both use a combination of Calendar and WhatsApp as interfaces.

- **Calendar** will be used to capture objective, criteria, time attributes, availability, and confirmation of action.
- **WhatsApp** will be used to facilitate communication between consumers and Courier Service Providers as well as their respective Fetch AI agents.

### Consumer Journey

Consumers will communicate with their individual coordinating agents that will have access to and interact with consumers' calendars and WhatsApp on their behalf to autonomously find a courier. The consumer’s journey includes:

- Putting an objective (in natural language text) in their calendar for a parcel pickup on a specific date and time.
- Adding additional criteria to help match the courier provider, such as:
  - Package pickup location (can default to ‘current location’ based on consumer’s GPS location)
  - Package drop-off location
  - Package dimensions & weight (restricted to letter parcels only)
  - Price
  - Desired delivery time

### Courier Provider Journey

Courier service providers will communicate with their individual coordinating agents that will have access to and interact with providers' calendars and WhatsApp on their behalf to autonomously find consumers. The provider’s journey includes:

- Putting an objective (in natural language text) in their calendar for a parcel delivery on a specific date and time.
- Adding criteria to match consumer requirements, such as:
  - Pickup location
  - Drop-off location
  - Package dimensions & weight
  - Price
  - Delivery time availability

## Go To Market Strategy

Define a go-to-market strategy that is complete with hypotheses, projections, and analysis of the initial city (or set of cities) picked for launch. Include marketing tactics to bootstrap Consumers and Courier Service Providers. This needs to be executable to truly launch this marketplace.

## HARDWARE & SOFTWARE REQUIREMENTS

### SOFTWARE REQUIRED

- **Fetch Technologies**
  - Agents using Fetch’s Python-based agent framework
  - Fetch platform
    - Interfacing with the Fetch’s AI Engine
    - Using Fetch’s managed agents
    - Using Agentverse console for hosting, listing, and analytics of managed agents
    - Utilizing other features of Agentverse

---
