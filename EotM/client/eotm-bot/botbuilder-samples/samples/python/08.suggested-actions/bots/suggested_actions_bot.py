# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions
import sys
sys.path.append('/Users/vaheh/Downloads/Thesis/myinalyze/EotM/client/')
from dataAggregator import DataAggregator

getData = DataAggregator()
trends = getData.indexer()
ubertrends={}

for obj in trends:
    for key, value in obj.items():
        if key not in ['related_topics']:
            ubertrends[key] = value

#print('not sorted ubertrends ==> ', ubertrends)
sorted_trends = sorted(ubertrends.items(), key= lambda x: x[1], reverse=True)
#print('sorted trends ==>', sorted_trends)



class SuggestActionsBot(ActivityHandler):
    """
    This bot will respond to the user's input with suggested actions.
    Suggested actions enable your bot to present buttons that the user
    can tap to provide input.
    """

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        """
        Send a welcome message to the user and tell them what actions they may perform to use this bot
        """

        return await self._send_welcome_message(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to the users choice and display the suggested actions again.
        """

        text = turn_context.activity.text.lower()
        response_text = self._process_input(text)

        await turn_context.send_activity(MessageFactory.text(response_text))


        # for key, value in ubertrends.items():
        #     print(key)
        #     if text == key.lower():

        return await self._send_suggested_actions(turn_context, followUp='PickATrend')

            # else:
            #     return await self._send_suggested_actions(turn_context, followUp='firstQ')



    async def _send_welcome_message(self, turn_context: TurnContext):
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Welcome to EotM Bot {member.name}. "
                        "EotM or Eyes On The Market is designed to provide the Product Owner and the team with the current word on the market. "
                        "It first identifies the trending topics, then crawls the web and finds out how often each of those topics is discussed about on"
                        " different platforms."
                        " After aggregating the results, it can show you the trending topics in an ordered manner."
                        " This helps the PO have a general idea about what the market is talking about."
                    + " This bot can show you the current trends in the market."
                    + f" Please answer the question: "
                    )
                )

                await self._send_suggested_actions(turn_context)



    def _process_input(self, text: str):

        related_topics_trend = {}

        if text in ["show me all trends", "all trends", "show me all topics"]:
            i=1
            response ='Here is an overview of all the trends and topics currently being discussed on the market, ' \
                      'in a descending order for popularity.\n'
            for trend in ubertrends:


                response += str(i)+". "+ trend+'\n'
                i+=1

            i=1
            return response

        if text == "show me a trend in a specific area":

            return "Which trend would you be interested in?"

        if text == "tell me more about yourself first":

            return "I use trends specified by market research websites as a starting point. Then I crawl websites such as TechCrunch, Twitter, and Google index" \
                   " to find how hyped the identified trends are. I then aggregate the results from different sources and present the ordered list to you. " \
                   " This helps you have a general idea about what the market is talking about, and use the insights in sprint planning, backlog " \
                   "prioritization and strategy setting.\n Would you be interested to see the trends in a specific area, or would you like to see an overview " \
                   "of all trends? \n You can choose below."


        for obj in trends:
            for key, value in obj.items():

                if text == key.lower():

                    for keys, values in obj['related_topics'].items():
                        related_topics_trend[keys] = values


                    sorted_trends_relatedTopics = sorted(related_topics_trend.items(), key=lambda x: x[1], reverse=True)


                    i=1
                    response =f"Showing you trends in {text} area.\n People are currently talking about these topics, in this order.\n" \
                              f" So, the first topic below is the most talked about in {text} area.\n"

                    for trend in sorted_trends_relatedTopics:
                        response += str(i) + ". " + trend[0] + '\n'
                        i += 1

                    i = 1

                    response += '\n'+ 'Would you like to see trends in another area?'

                    return response

        return "I'm not sure how I can help you. Would you be interested to see the trends in a specific area, or would you like to see an overview " \
                   "of all trends? \n You can choose below."

    async def _send_suggested_actions(self, turn_context: TurnContext, followUp='firstQ'):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """


        if followUp == 'firstQ':

            reply = MessageFactory.text("Would you like to see an overview of all the trends, or are you interested in a specific trend?")

            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(title="Show me all trends", type=ActionTypes.im_back, value="All Trends"),
                    CardAction(title="Show me a trends in a specific area", type=ActionTypes.im_back, value="Show me a trend in a specific area"),
                    CardAction(title="Tell me more about yourself first", type=ActionTypes.im_back,
                               value="Tell me more about yourself first")
                ]
            )

            return await turn_context.send_activity(reply)



        if followUp == 'PickATrend':

            reply = MessageFactory.text("")

            actions = []
            actions.append(CardAction(title="Show me all trends", type=ActionTypes.im_back, value="All Trends"))
            for trend in ubertrends:
                actions.append(CardAction(title=trend, type=ActionTypes.im_back, value=trend))

            actions.append(CardAction(title="Tell me more about yourself first", type=ActionTypes.im_back,
                       value="Tell me more about yourself first"))


            reply.suggested_actions = SuggestedActions(actions=actions)

            return await turn_context.send_activity(reply)






