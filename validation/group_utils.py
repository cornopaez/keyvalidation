from .models import Account, KeyGroup
from django.db.models import Q, Prefetch

def get_valid_groups(serial_data):
    # Fetch active groups for acct where there's overlap between the start/end numbers
    existing_groups = (Account.objects
        .prefetch_related(
            Prefetch(
                'key_groups',
                queryset=(KeyGroup.objects
                    .filter(
                        (
                            Q(
                                doc_num_start__lte=serial_data['doc_num_start'], 
                                doc_num_end__gte=serial_data['doc_num_end']
                            )
                            | 
                            Q(
                                doc_num_start__lte=serial_data['doc_num_start'], 
                                doc_num_end__gte=serial_data['doc_num_start']
                            ) 
                            | 
                            Q(
                                doc_num_start__lte=serial_data['doc_num_end'], 
                                doc_num_end__gte=serial_data['doc_num_end']
                            )
                        )
                        &
                        (
                            Q(exhausted__exact=False)
                        )
                    )
                ),
                to_attr='filtered_key_groups'
            )
        )
        .get(
            number=serial_data['account'],
            bank=serial_data['bank'],
            source=serial_data['source'],
        )
    )

    return existing_groups