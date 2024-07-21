from ai_engine import Model, Context, agent, Protocol, UAgentResponse, KeyValue

class ConsumerAgentMapping(Model):
    email: str
    address: str

class ProviderRegistrationRequest(Model):
    provider_agent: str

adapter_protocol = Protocol(f"Courier Marketplace adapter protocol")

@agent.on_event("startup")
async def initialize_mapping(ctx: Context):
    # Initialize the mapping dictionaries
    ctx.storage.set("consumer_provider_mapping", {})
    ctx.storage.set("all_providers", [])

@adapter_protocol.on_message(model=ConsumerAgentMapping)
async def register_consumer(ctx: Context, sender: str, msg: ConsumerAgentMapping):
    # Update consumer-provider mapping
    consumer_mapping = ctx.storage.get("consumer_provider_mapping")
    consumer_mapping[msg.email] = msg.address
    ctx.storage.set("consumer_provider_mapping", consumer_mapping)

@adapter_protocol.on_message(model=ProviderRegistrationRequest)
async def register_provider(ctx: Context, sender: str, msg: ProviderRegistrationRequest):
    # Update provider list
    all_providers = ctx.storage.get("all_providers", [])
    all_providers.append(msg.provider_agent)
    ctx.storage.set("all_providers", all_providers)

@adapter_protocol.on_message(model=Request, replies=UAgentResponse)
async def send_to_provider(ctx: Context, sender: str, msg: Request):
    # Generate a unique request ID
    request_id = datetime.now().strftime("%Y%m%d%H%M%S")
    await ctx.send(sender, UAgentResponse(request_id=request_id))

    # Save provider addresses for available providers only
    provider_addresses = {}
    for index, provider in enumerate(ctx.storage.get("all_providers")):
        provider_addresses[index] = provider
    ctx.storage.set(request_id, provider_addresses)

@adapter_protocol.on_message(model=Response)
async def response_from_provider(ctx: Context, sender: str, msg: Response):
    ctx.logger.info(f"session in response_from_provider: {ctx.session}")
    ctx.logger.info(f"Message from provider: {msg.is_available}")

    # Retrieve provider availability dictionary
    provider_availability = ctx.storage.get("provider_availability", {})

    # Update provider availability for the current session
    provider_availability[ctx.session][sender] = msg.is_available

    # Check if all providers have responded
    if len(provider_availability[ctx.session]) == len(ctx.storage.get("all_providers")):
        ctx.logger.info(f"All providers have responded.")

        # Retrieve provider addresses for options
        provider_addresses = ctx.storage.get(ctx.session, {})

        # Prepare options for final response
        options = [KeyValue(key=f"provider_{index}", value=address) for index, address in provider_addresses.items()]

        # Send final response back to DeltaV
        await ctx.send(ctx.storage.get("deltav-sender"), UAgentResponse(options=options, type=UAgentResponseType.FINAL_OPTIONS))

    # Save updated provider availability
    ctx.storage.set("provider_availability", provider_availability)

@adapter_protocol.on_message(model=BookingRequest, replies=UAgentResponse)
async def handle_booking_request(ctx: Context, sender: str, msg: BookingRequest):
    # Retrieve provider address based on request_id and option index
    provider_addresses = ctx.storage.get(msg.request_id, {})
    provider_address = provider_addresses.get(msg.option_index)

    if provider_address:
        # Send event creation request to provider
        await ctx.send(provider_address, msg)

        # Retrieve consumer email to address mapping
        consumer_mapping = ctx.storage.get("consumer_provider_mapping")
        consumer_address = consumer_mapping.get(msg.consumer_email)

        if consumer_address:
            # Send WhatsApp message to consumer
            await ctx.send(consumer_address, "Your booking has been confirmed.")

agent.include(adapter_protocol)
