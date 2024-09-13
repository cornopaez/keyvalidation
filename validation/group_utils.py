from .models import Account, KeyGroup
from django.db.models import Q, Prefetch

def get_valid_groups(serial_data):
    # print(serial_data)
    # # Check values provided
    # if not isinstance(serial_data['account'], int) or serial_data['account'] <= 0:
    #     raise ValueError(f'Account number must be a positive integer.\n {serial_data['account']} {type(serial_data['account'])}')

    # if not isinstance(serial_data['doc_num_start'], int) or not isinstance(serial_data['doc_num_end'], int):
    #     raise TypeError(f'Values provided for start and finish must be integers.\n doc_num_start: {type(serial_data['doc_num_start'])}\n doc_num_start: {type(serial_data['doc_num_end'])}')

    # if serial_data['doc_num_start'] < 0 or serial_data['doc_num_end'] <0:
    #     raise ValueError(f'Values provided must be greater than zero.\n doc_num_start: {serial_data['doc_num_start']}\n doc_num_end: {serial_data['doc_num_end']}')

    # if serial_data['doc_num_end'] <= serial_data['doc_num_start']:
    #     raise ValueError(f'Document end number cannot be less or equal than the document start number.\n doc_num_start: {serial_data['doc_num_start']}\n doc_num_end: {serial_data['doc_num_end']}')

    # Fetch active groups for acct where there's overlap between the start/end numbers
    existing_groups = (Account.objects
        .prefetch_related(
            Prefetch(
                'key_groups',
                queryset=(KeyGroup.objects
                    .filter(
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

    # print(existing_groups.query)

    return existing_groups