from models import Feedback
from database import db_session
import graphene
from graphene import relay, Field, String, Int, DateTime
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql import GraphQLError


class FeedbackObject(SQLAlchemyObjectType):
    class Meta:
        model = Feedback
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    feedback = SQLAlchemyConnectionField(FeedbackObject.connection)


class AddFeedback(graphene.Mutation):
    class Arguments:
        address = String(required=True)
        name = String(required=True)
        email = String(required=True)
        message = String(required=True)
        created = DateTime(required=True)

    feedback = Field(FeedbackObject)

    def mutate(self, info, address, name, email, message, created):
        n_fb = Feedback(address, name, email, message, created)
        db_session.add(n_fb)
        db_session.commit()

        return AddFeedback(feedback=n_fb)


class UpdateFeedback(graphene.Mutation):
    class Arguments:
        fbid = Int(required=True)
        address = String()
        name = String()
        email = String()
        message = String()

    feedback = Field(FeedbackObject)

    def mutate(self, info, *args, **kwargs):
        feedback_fields = ['address', 'name', 'email', 'message']

        fb = db_session.query(Feedback).filter_by(
            fbid=kwargs.get('fbid')).first()

        fb.update(dict((key, kwargs[key])
                       for key in feedback_fields if key in kwargs))
        db_session.commit()

        return UpdateFeedback(feedback=fb)


class RemoveFeedback(graphene.Mutation):
    class Arguments:
        fbid = Int(required=True)

    feedback = Field(FeedbackObject)

    def mutate(self, info, fbid):
        fb = db_session.query(Feedback).filter_by(
            fbid=fbid).first()
        db_session.delete(fb)
        db_session.commit()

        return RemoveFeedback(feedback=fb)


class Mutation(graphene.ObjectType):
    addFeedback = AddFeedback.Field()
    updateFeedback = UpdateFeedback.Field()
    removeFeedback = RemoveFeedback.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
